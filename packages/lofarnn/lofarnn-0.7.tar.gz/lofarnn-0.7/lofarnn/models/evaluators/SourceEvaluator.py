# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import contextlib
import copy
import io
import itertools
import json
import logging
import numpy as np
import os
import pickle
from collections import OrderedDict
import pycocotools.mask as mask_util
import torch
from fvcore.common.file_io import PathManager
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from tabulate import tabulate

import detectron2.utils.comm as comm
from detectron2.data import MetadataCatalog
from detectron2.data.datasets.coco import convert_to_coco_json
from detectron2.structures import Boxes, BoxMode, pairwise_iou
from detectron2.utils.logger import create_small_table

from detectron2.evaluation.evaluator import DatasetEvaluator


class SourceEvaluator(DatasetEvaluator):
    """
    Evaluate object proposal, instance detection/segmentation, keypoint detection
    outputs using COCO's metrics and APIs. But only do the bboxes with the one with the single highest confidence

    Calculates it over multi-component, single-component, and size-limited subsets

    """

    def __init__(
        self, dataset_name, cfg, distributed, output_dir=None, physical_cut_dict=None
    ):
        """
        Args:
            dataset_name (str): name of the dataset to be evaluated.
                It must have either the following corresponding metadata:

                    "json_file": the path to the COCO format annotation

                Or it must be in detectron2's standard dataset format
                so it can be converted to COCO format automatically.
            cfg (CfgNode): config instance
            distributed (True): if True, will collect results from all ranks and run evaluation
                in the main process.
                Otherwise, will evaluate the results in the current process.
            output_dir (str): optional, an output directory to dump all
                results predicted on the dataset. The dump contains two files:

                1. "instance_predictions.pth" a file in torch serialization
                   format that contains all the raw original predictions.
                2. "coco_instances_results.json" a json file in COCO's result
                   format.
            physical_cut_dict (dict): Optional, Dictionary mapping Source Names to multicomponent,
             single component, and size cuts, should be in format of {cut: [list]} where list is the Source Names for that cut
        """
        self._tasks = self._tasks_from_config(cfg)
        self._distributed = distributed
        self._output_dir = output_dir
        self._physical_cuts = physical_cut_dict

        self._cpu_device = torch.device("cpu")
        self._logger = logging.getLogger(__name__)
        self._dataset_name = dataset_name

        self._metadata = MetadataCatalog.get(dataset_name)
        if not hasattr(self._metadata, "json_file"):
            self._logger.warning(
                f"json_file was not found in MetaDataCatalog for '{dataset_name}'."
                " Trying to convert it to COCO format ..."
            )

            cache_path = os.path.join(output_dir, f"{dataset_name}_coco_format.json")
            self._metadata.json_file = cache_path
            convert_to_coco_json(dataset_name, cache_path)

        json_file = PathManager.get_local_path(self._metadata.json_file)
        with contextlib.redirect_stdout(io.StringIO()):
            self._coco_api = COCO(json_file)

        self._kpt_oks_sigmas = cfg.TEST.KEYPOINT_OKS_SIGMAS
        # Test set json files do not contain annotations (evaluation must be
        # performed using the COCO evaluation server).
        self._do_evaluation = "annotations" in self._coco_api.dataset

    def reset(self):
        self._predictions = []

    def _tasks_from_config(self, cfg):
        """
        Returns:
            tuple[str]: tasks that can be evaluated under the given configuration.
        """
        tasks = ("bbox",)
        if cfg.MODEL.MASK_ON:
            tasks = tasks + ("segm",)
        if cfg.MODEL.KEYPOINT_ON:
            tasks = tasks + ("keypoints",)
        return tasks

    def process(self, inputs, outputs):
        """
        Args:
            inputs: the inputs to a COCO model (e.g., GeneralizedRCNN).
                It is a list of dict. Each dict corresponds to an image and
                contains keys like "height", "width", "file_name", "image_id".
            outputs: the outputs of a COCO model. It is a list of dicts with key
                "instances" that contains :class:`Instances`.
        """
        for input, output in zip(inputs, outputs):
            if ".npy" in input["file_name"]:
                source_name = input["file_name"].split("/")[-1].split(".npy")[0]
            else:
                source_name = input["file_name"].split("/")[-1].split(".png")[0]
            prediction = {
                "image_id": input["image_id"],
                "source_name": source_name,
            }  # Add Name to get component later

            # TODO this is ugly
            if "instances" in output:
                instances = output["instances"].to(self._cpu_device)
                prediction["instances"] = instances_to_coco_json(
                    instances, input["image_id"]
                )
            if "proposals" in output:
                prediction["proposals"] = output["proposals"].to(self._cpu_device)
            self._predictions.append(prediction)

    def evaluate(self):
        if self._distributed:
            comm.synchronize()
            predictions = comm.gather(self._predictions, dst=0)
            predictions = list(itertools.chain(*predictions))

            if not comm.is_main_process():
                return {}
        else:
            predictions = self._predictions

        if len(predictions) == 0:
            self._logger.warning("[COCOEvaluator] Did not receive valid predictions.")
            return {}

        if self._output_dir:
            PathManager.mkdirs(self._output_dir)
            file_path = os.path.join(self._output_dir, "instances_predictions.pth")
            with PathManager.open(file_path, "wb") as f:
                torch.save(predictions, f)

        self._results = OrderedDict()
        if "proposals" in predictions[0]:
            self._eval_box_proposals(predictions)
        if "instances" in predictions[0]:
            self._eval_predictions(set(self._tasks), predictions)
        # Copy so the caller can do whatever with results
        return copy.deepcopy(self._results)

    def _eval_predictions(self, tasks, predictions):
        """
        Evaluate predictions on the given tasks.
        Fill self._results with the metrics of the tasks.
        """
        self._logger.info("Preparing results for COCO format ...")
        coco_results = list(itertools.chain(*[x["instances"] for x in predictions]))

        # unmap the category ids for COCO
        if hasattr(self._metadata, "thing_dataset_id_to_contiguous_id"):
            reverse_id_mapping = {
                v: k
                for k, v in self._metadata.thing_dataset_id_to_contiguous_id.items()
            }
            for result in coco_results:
                category_id = result["category_id"]
                assert (
                    category_id in reverse_id_mapping
                ), "A prediction has category_id={}, which is not available in the dataset.".format(
                    category_id
                )
                result["category_id"] = reverse_id_mapping[category_id]

        if self._output_dir:
            file_path = os.path.join(self._output_dir, "coco_instances_results.json")
            self._logger.info("Saving results to {}".format(file_path))
            with PathManager.open(file_path, "w") as f:
                f.write(json.dumps(coco_results))
                f.flush()

        if not self._do_evaluation:
            self._logger.info("Annotations are not available for evaluation.")
            return

        # Calculate the recall based on general recall and precision, not COCO mAP, with single best prediction
        self._logger.info(f"Evaluating with non-mAR...")
        all_recall = _evaluate_box_proposals(predictions, self._coco_api, limit=1)
        pickle.dump(
            all_recall["per_source"],
            file=open(
                os.path.join(
                    self._output_dir, f"{self._dataset_name}_recall_limit1.pkl"
                ),
                "wb",
            ),
        )
        self._results["own_recall"] = {
            "ar": all_recall["ar"],
            "ap": all_recall["ap"],
            "precision": all_recall["precisions"][-1],
            "recall": all_recall["recalls"][-1],
        }
        all_recall = _evaluate_box_proposals(predictions, self._coco_api, limit=2)
        pickle.dump(
            all_recall["per_source"],
            file=open(
                os.path.join(
                    self._output_dir, f"{self._dataset_name}_recall_limit2.pkl"
                ),
                "wb",
            ),
        )
        self._results["own_recall_2"] = {
            "ar": all_recall["ar"],
            "ap": all_recall["ap"],
            "precision": all_recall["precisions"][-1],
            "recall": all_recall["recalls"][-1],
        }
        all_recall = _evaluate_box_proposals(predictions, self._coco_api, limit=5)
        pickle.dump(
            all_recall["per_source"],
            file=open(
                os.path.join(
                    self._output_dir, f"{self._dataset_name}_recall_limit5.pkl"
                ),
                "wb",
            ),
        )
        self._results["own_recall_5"] = {
            "ar": all_recall["ar"],
            "ap": all_recall["ap"],
            "precision": all_recall["precisions"][-1],
            "recall": all_recall["recalls"][-1],
        }
        all_recall = _evaluate_box_proposals(predictions, self._coco_api, limit=10)
        pickle.dump(
            all_recall["per_source"],
            file=open(
                os.path.join(
                    self._output_dir, f"{self._dataset_name}_recall_limit10.pkl"
                ),
                "wb",
            ),
        )
        self._results["own_recall_10"] = {
            "ar": all_recall["ar"],
            "ap": all_recall["ap"],
            "precision": all_recall["precisions"][-1],
            "recall": all_recall["recalls"][-1],
        }
        all_recall = _evaluate_box_proposals(predictions, self._coco_api, limit=100)
        pickle.dump(
            all_recall["per_source"],
            file=open(
                os.path.join(
                    self._output_dir, f"{self._dataset_name}_recall_limit100.pkl"
                ),
                "wb",
            ),
        )
        self._results["own_recall_100"] = {
            "ar": all_recall["ar"],
            "ap": all_recall["ap"],
            "precision": all_recall["precisions"][-1],
            "recall": all_recall["recalls"][-1],
        }
        for physical_cut in self._physical_cuts.keys():
            self._logger.info(
                f"Evaluating with non-mAR on physical cut {physical_cut}..."
            )
            prediction_cut = self._get_physical_cut_predictions(
                physical_cut, predictions
            )
            # physical_coco_results = list(itertools.chain(*[x["instances"] for x in prediction_cut]))
            phys_recall = _evaluate_box_proposals(
                prediction_cut, self._coco_api, limit=1
            )
            recall_name = f"own_recall_{physical_cut}"
            self._results[recall_name] = {
                "ar": phys_recall["ar"],
                "ap": phys_recall["ap"],
                "precision": phys_recall["precisions"][-1],
                "recall": phys_recall["recalls"][-1],
            }
            phys_recall = _evaluate_box_proposals(
                prediction_cut, self._coco_api, limit=2
            )
            recall_name = f"own_recall_2_{physical_cut}"
            self._results[recall_name] = {
                "ar": phys_recall["ar"],
                "ap": phys_recall["ap"],
                "precision": phys_recall["precisions"][-1],
                "recall": phys_recall["recalls"][-1],
            }
            phys_recall = _evaluate_box_proposals(
                prediction_cut, self._coco_api, limit=5
            )
            recall_name = f"own_recall_5_{physical_cut}"
            self._results[recall_name] = {
                "ar": phys_recall["ar"],
                "ap": phys_recall["ap"],
                "precision": phys_recall["precisions"][-1],
                "recall": phys_recall["recalls"][-1],
            }
            phys_recall = _evaluate_box_proposals(
                prediction_cut, self._coco_api, limit=10
            )
            recall_name = f"own_recall_10_{physical_cut}"
            self._results[recall_name] = {
                "ar": phys_recall["ar"],
                "ap": phys_recall["ap"],
                "precision": phys_recall["precisions"][-1],
                "recall": phys_recall["recalls"][-1],
            }
            phys_recall = _evaluate_box_proposals(
                prediction_cut, self._coco_api, limit=100
            )
            recall_name = f"own_recall_100_{physical_cut}"
            self._results[recall_name] = {
                "ar": phys_recall["ar"],
                "ap": phys_recall["ap"],
                "precision": phys_recall["precisions"][-1],
                "recall": phys_recall["recalls"][-1],
            }
        self._logger.info("Evaluating predictions ...")
        for task in sorted(tasks):
            coco_eval = (
                _evaluate_predictions_on_coco(
                    self._coco_api,
                    coco_results,
                    task,
                    kpt_oks_sigmas=self._kpt_oks_sigmas,
                )
                if len(coco_results) > 0
                else None  # cocoapi does not handle empty results very well
            )
            res = self._derive_coco_results(
                coco_eval, task, class_names=self._metadata.get("thing_classes")
            )
            self._results[task] = res
        for physical_cut in self._physical_cuts.keys():
            self._logger.info(f"Evaluating on physical cut {physical_cut}...")
            prediction_cut = self._get_physical_cut_predictions(
                physical_cut, predictions
            )
            physical_coco_results = list(
                itertools.chain(*[x["instances"] for x in prediction_cut])
            )
            for task in sorted(tasks):
                coco_eval = (
                    _evaluate_predictions_on_coco(
                        self._coco_api,
                        physical_coco_results,
                        task,
                        kpt_oks_sigmas=self._kpt_oks_sigmas,
                    )
                    if len(physical_coco_results) > 0
                    else None  # cocoapi does not handle empty results very well
                )
                res = self._derive_coco_results(
                    coco_eval, task, class_names=self._metadata.get("thing_classes")
                )
                result_name = f"{task}_{physical_cut}"
                self._results[result_name] = res

    def _get_physical_cut_predictions(self, cut_key, predictions):
        prediction_cut = []
        for prediction in predictions:
            if prediction["source_name"] in self._physical_cuts[cut_key]:
                prediction_cut.append(prediction)
            elif (
                prediction["source_name"].rpartition(".")[0]
                in self._physical_cuts[cut_key]
            ):
                # Handles the rotation, where there is an extra '.rot' after the source name
                prediction_cut.append(prediction)
        return prediction_cut

    def _derive_coco_results(self, coco_eval, iou_type, class_names=None):
        """
        Derive the desired score numbers from summarized COCOeval.

        Args:
            coco_eval (None or COCOEval): None represents no predictions from model.
            iou_type (str):
            class_names (None or list[str]): if provided, will use it to predict
                per-category AP.

        Returns:
            a dict of {metric name: score}
        """

        metrics = {
            "bbox": [
                "AP",
                "AP50",
                "AP75",
                "APs",
                "APm",
                "APl",
                "AR",
                "AR50",
                "AR75",
                "ARs",
                "ARm",
                "ARl",
            ],
            "segm": [
                "AP",
                "AP50",
                "AP75",
                "APs",
                "APm",
                "APl",
                "AR",
                "AR50",
                "AR75",
                "ARs",
                "ARm",
                "ARl",
            ],
            "keypoints": ["AP", "AP50", "AP75", "APm", "APl"],
        }[iou_type]

        if coco_eval is None:
            self._logger.warn("No predictions from the model!")
            return {metric: float("nan") for metric in metrics}

        # the standard metrics
        results = {
            metric: float(
                coco_eval.stats[idx] * 100 if coco_eval.stats[idx] >= 0 else "nan"
            )
            for idx, metric in enumerate(metrics)
        }
        self._logger.info(
            "Evaluation results for {}: \n".format(iou_type)
            + create_small_table(results)
        )
        if not np.isfinite(sum(results.values())):
            self._logger.info("Note that some metrics cannot be computed.")

        if class_names is None or len(class_names) <= 1:
            return results
        # Compute per-category AP
        # from https://github.com/facebookresearch/Detectron/blob/a6a835f5b8208c45d0dce217ce9bbda915f44df7/detectron/datasets/json_dataset_evaluator.py#L222-L252 # noqa
        precisions = coco_eval.eval["recall"]
        # precision has dims (iou, recall, cls, area range, max dets)
        assert len(class_names) == precisions.shape[2]

        results_per_category = []
        for idx, name in enumerate(class_names):
            # area range index 0: all area ranges
            # max dets index -1: typically 100 per image
            precision = precisions[:, :, idx, 0, -1]
            precision = precision[precision > -1]
            ap = np.mean(precision) if precision.size else float("nan")
            results_per_category.append(("{}".format(name), float(ap * 100)))

        # tabulate it
        N_COLS = min(6, len(results_per_category) * 2)
        results_flatten = list(itertools.chain(*results_per_category))
        results_2d = itertools.zip_longest(
            *[results_flatten[i::N_COLS] for i in range(N_COLS)]
        )
        table = tabulate(
            results_2d,
            tablefmt="pipe",
            floatfmt=".3f",
            headers=["category", "AP"] * (N_COLS // 2),
            numalign="left",
        )
        self._logger.info("Per-category {} AP: \n".format(iou_type) + table)

        results.update({"AP-" + name: ap for name, ap in results_per_category})
        return results


def instances_to_coco_json(instances, img_id):
    """
    Dump an "Instances" object to a COCO-format json that's used for evaluation.

    Args:
        instances (Instances):
        img_id (int): the image id

    Returns:
        list[dict]: list of json annotations in COCO format.
    """
    num_instance = len(instances)
    if num_instance == 0:
        return []

    boxes = instances.pred_boxes.tensor.numpy()
    boxes = BoxMode.convert(boxes, BoxMode.XYXY_ABS, BoxMode.XYWH_ABS)
    boxes = boxes.tolist()
    scores = instances.scores.tolist()
    classes = instances.pred_classes.tolist()

    has_mask = instances.has("pred_masks")
    if has_mask:
        # use RLE to encode the masks, because they are too large and takes memory
        # since this evaluator stores outputs of the entire dataset
        rles = [
            mask_util.encode(np.array(mask[:, :, None], order="F", dtype="uint8"))[0]
            for mask in instances.pred_masks
        ]
        for rle in rles:
            # "counts" is an array encoded by mask_util as a byte-stream. Python3's
            # json writer which always produces strings cannot serialize a bytestream
            # unless you decode it. Thankfully, utf-8 works out (which is also what
            # the pycocotools/_mask.pyx does).
            rle["counts"] = rle["counts"].decode("utf-8")

    has_keypoints = instances.has("pred_keypoints")
    if has_keypoints:
        keypoints = instances.pred_keypoints

    results = []
    for k in range(num_instance):
        result = {
            "image_id": img_id,
            "category_id": classes[k],
            "bbox": boxes[k],
            "score": scores[k],
        }
        if has_mask:
            result["segmentation"] = rles[k]
        if has_keypoints:
            # In COCO annotations,
            # keypoints coordinates are pixel indices.
            # However our predictions are floating point coordinates.
            # Therefore we subtract 0.5 to be consistent with the annotation format.
            # This is the inverse of data loading logic in `datasets/coco.py`.
            keypoints[k][:, :2] -= 0.5
            result["keypoints"] = keypoints[k].flatten().tolist()
        results.append(result)
    return results


# inspired from Detectron:
# https://github.com/facebookresearch/Detectron/blob/a6a835f5b8208c45d0dce217ce9bbda915f44df7/detectron/datasets/json_dataset_evaluator.py#L255 # noqa
def _evaluate_box_proposals(
    dataset_predictions, coco_api, thresholds=None, area="all", limit=None
):
    """
    Evaluate detection proposal recall metrics. This function is a much
    faster alternative to the official COCO API recall evaluation code. However,
    it produces slightly different results.
    """
    # Record max overlap value for each gt box
    # Return vector of overlap values
    areas = {
        "all": 0,
        "small": 1,
        "medium": 2,
        "large": 3,
        "96-128": 4,
        "128-256": 5,
        "256-512": 6,
        "512-inf": 7,
    }
    area_ranges = [
        [0 ** 2, 1e5 ** 2],  # all
        [0 ** 2, 32 ** 2],  # small
        [32 ** 2, 96 ** 2],  # medium
        [96 ** 2, 1e5 ** 2],  # large
        [96 ** 2, 128 ** 2],  # 96-128
        [128 ** 2, 256 ** 2],  # 128-256
        [256 ** 2, 512 ** 2],  # 256-512
        [512 ** 2, 1e5 ** 2],
    ]  # 512-inf
    assert area in areas, "Unknown area range: {}".format(area)
    area_range = area_ranges[areas[area]]
    gt_overlaps = []
    num_pos = 0
    num_boxes = 0
    source_outcomes = {}
    for prediction_dict in dataset_predictions:
        preds = np.asarray(prediction_dict["instances"])
        scores = []
        for i in preds:
            scores.append(i["score"])

        # sort predictions in descending order
        # TODO maybe remove this and make it explicit in the documentation
        inds = (-1 * np.asarray(scores)).argsort()
        preds = preds[inds]

        ann_ids = coco_api.getAnnIds(imgIds=prediction_dict["image_id"])
        anno = coco_api.loadAnns(ann_ids)
        gt_boxes = [
            BoxMode.convert(obj["bbox"], BoxMode.XYWH_ABS, BoxMode.XYXY_ABS)
            for obj in anno
            if obj["iscrowd"] == 0
        ]
        gt_boxes = torch.as_tensor(gt_boxes).reshape(-1, 4)  # guard against no boxes
        gt_boxes = Boxes(gt_boxes)
        gt_areas = torch.as_tensor([obj["area"] for obj in anno if obj["iscrowd"] == 0])

        if len(gt_boxes) == 0 or len(preds) == 0:
            continue

        valid_gt_inds = (gt_areas >= area_range[0]) & (gt_areas <= area_range[1])
        gt_boxes = gt_boxes[valid_gt_inds]

        num_pos += len(gt_boxes)  # 1 GT from each image
        num_boxes += limit  # N number of proposals kept

        if len(gt_boxes) == 0:
            continue

        if limit is not None and len(preds) > limit:
            preds = preds[:limit]

        pred_boxes = []
        for i in preds:
            pred_boxes.append(
                BoxMode.convert(i["bbox"], BoxMode.XYWH_ABS, BoxMode.XYXY_ABS)
            )
        pred_boxes = torch.as_tensor(pred_boxes).reshape(
            -1, 4
        )  # guard against no boxes
        pred_boxes = Boxes(pred_boxes)
        overlaps = pairwise_iou(pred_boxes, gt_boxes)

        _gt_overlaps = torch.zeros(len(gt_boxes))
        for j in range(min(len(preds), len(gt_boxes))):
            # find which proposal box maximally covers each gt box
            # and get the iou amount of coverage for each gt box
            max_overlaps, argmax_overlaps = overlaps.max(dim=0)

            # find which gt box is 'best' covered (i.e. 'best' = most iou)
            gt_ovr, gt_ind = max_overlaps.max(dim=0)
            assert gt_ovr >= 0
            # find the proposal box that covers the best covered gt box
            box_ind = argmax_overlaps[gt_ind]
            # record the iou coverage of this gt box
            _gt_overlaps[j] = overlaps[box_ind, gt_ind]
            assert _gt_overlaps[j] == gt_ovr
            # mark the proposal box and the gt box as used
            overlaps[box_ind, :] = -1
            overlaps[:, gt_ind] = -1
            print(preds[gt_ind])
            source_outcomes[
                prediction_dict["source_name"]
            ] = gt_ovr.item()  # Save overlap, so can be used for determining outcome

        # append recorded iou coverage level
        gt_overlaps.append(_gt_overlaps)
    gt_overlaps = (
        torch.cat(gt_overlaps, dim=0)
        if len(gt_overlaps)
        else torch.zeros(0, dtype=torch.float32)
    )
    gt_overlaps, _ = torch.sort(gt_overlaps)

    if thresholds is None:
        step = 0.05
        thresholds = torch.arange(0.5, 0.95 + 1e-5, step, dtype=torch.float32)
    recalls = torch.zeros_like(thresholds)
    precisions = torch.zeros_like(thresholds)
    # compute recall for each iou threshold
    for i, t in enumerate(thresholds):
        recalls[i] = (gt_overlaps >= t).float().sum() / float(
            num_pos
        )  # TP/(Num GT Labels) with GT being Num Images as 1 GT per image
    for i, t in enumerate(thresholds):
        precisions[i] = (gt_overlaps >= t).float().sum() / float(
            num_boxes
        )  # TP/(Num of boxes kept)
    # ar = 2 * np.trapz(recalls, thresholds)
    ar = recalls.mean()
    ap = precisions.mean()
    return {
        "ar": ar,
        "ap": ap,
        "per_source": source_outcomes,
        "recalls": recalls,
        "precisions": precisions,
        "thresholds": thresholds,
        "gt_overlaps": gt_overlaps,
        "num_pos": num_pos,
    }


def _evaluate_predictions_on_coco(coco_gt, coco_results, iou_type, kpt_oks_sigmas=None):
    """
    Evaluate the coco results using COCOEval API.
    """
    assert len(coco_results) > 0

    if iou_type == "segm":
        coco_results = copy.deepcopy(coco_results)
        # When evaluating mask AP, if the results contain bbox, cocoapi will
        # use the box area as the area of the instance, instead of the mask area.
        # This leads to a different definition of small/medium/large.
        # We remove the bbox field to let mask AP use mask area.
        for c in coco_results:
            c.pop("bbox", None)

    coco_dt = coco_gt.loadRes(coco_results)
    coco_eval = COCOeval(coco_gt, coco_dt, iou_type)
    # Use the COCO default keypoint OKS sigmas unless overrides are specified
    if kpt_oks_sigmas:
        coco_eval.params.kpt_oks_sigmas = np.array(kpt_oks_sigmas)

    if iou_type == "keypoints":
        num_keypoints = len(coco_results[0]["keypoints"]) // 3
        assert len(coco_eval.params.kpt_oks_sigmas) == num_keypoints, (
            "[COCOEvaluator] The length of cfg.TEST.KEYPOINT_OKS_SIGMAS (default: 17) "
            "must be equal to the number of keypoints. However the prediction has {} "
            "keypoints! For more information please refer to "
            "http://cocodataset.org/#keypoints-eval.".format(num_keypoints)
        )

    coco_eval.evaluate()
    coco_eval.accumulate()
    coco_eval.summarize()

    return coco_eval
