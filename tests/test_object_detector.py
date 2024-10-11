from nrtk_explorer.library import object_detector
from nrtk.impls.score_detections.coco_scorer import COCOScorer
from nrtk_explorer.library.coco_utils import (
    convert_from_ground_truth_to_first_arg,
    convert_from_predictions_to_second_arg,
)

import json
from utils import get_images, DATASET


def test_detector_small():
    sample = get_images()
    detector = object_detector.ObjectDetector(model_name="hustvl/yolos-tiny")
    img = detector.eval(sample)
    assert len(img) == len(sample.keys())


def test_nrkt_scorer():
    ds = json.load(open(DATASET))
    sample = get_images()
    detector = object_detector.ObjectDetector(model_name="facebook/detr-resnet-50")
    predictions = detector.eval(sample)

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

    image_count = len(sample.keys())
    assert len(predictions) == image_count
    assert len(score_output) == image_count
