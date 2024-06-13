from nrtk_explorer.library import object_detector
from nrtk.impls.score_detections.coco_scorer import COCOScorer
from nrtk_explorer.library.coco_utils import (
    convert_from_ground_truth_to_first_arg,
    convert_from_predictions_to_second_arg,
)

import json
import os
import nrtk_explorer.test_data

DIR_PATH = os.path.dirname(nrtk_explorer.test_data.__file__)
DATASET_PATH = f"{DIR_PATH}/coco-od-2017/"
DATASET = f"{DATASET_PATH}/test_val2017.json"


def test_detector_small():
    ds = json.load(open(DATASET))
    sample = [f"{DATASET_PATH}/{img['file_name']}" for img in ds["images"]][:15]
    detector = object_detector.ObjectDetector(model_name="hustvl/yolos-tiny")
    img = detector.eval(image_ids=sample)
    assert len(img) == 15


def test_nrkt_scorer():
    ds = json.load(open(DATASET))
    sample = [f"{DATASET_PATH}/{img['file_name']}" for img in ds["images"]]
    detector = object_detector.ObjectDetector(model_name="facebook/detr-resnet-50")
    predictions = detector.eval(image_ids=sample)

    dataset_annotations = dict()
    for annotation in ds["annotations"]:
        image_annotations = dataset_annotations.setdefault(annotation["image_id"], [])
        image_annotations.append(annotation)

    ground_truth_annotations = list()
    for img in ds["images"]:
        ground_truth_annotations.append(dataset_annotations[img["id"]])

    coco_ground_truth = convert_from_ground_truth_to_first_arg(ground_truth_annotations)
    coco_predictions = convert_from_predictions_to_second_arg(predictions)
    scorer = COCOScorer(DATASET)
    score_output = scorer.score(coco_ground_truth, coco_predictions)

    assert len(predictions) == 16
    assert len(score_output) == 16
