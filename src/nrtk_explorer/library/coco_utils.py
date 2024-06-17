from smqtk_image_io.bbox import AxisAlignedBoundingBox
from nrtk.impls.score_detections.class_agnostic_pixelwise_iou_scorer import (
    ClassAgnosticPixelwiseIoUScorer,
)
from typing import Sequence
from nrtk_explorer.app.image_ids import DatasetId

# This module contains functions to convert ground truth annotations and predictions to COCOScorer format
# COCOScorer is a library that computes the COCO metrics for object detection tasks.


def convert_from_ground_truth_to_first_arg(dataset_annotations):
    """Convert ground truth annotations to COCOScorer format"""
    annotations = list()
    for dataset_image_annotations in dataset_annotations:
        image_annotations = list()
        for annotation in dataset_image_annotations:
            image_annotations.append(
                (
                    AxisAlignedBoundingBox(
                        annotation["bbox"][0:2],
                        [
                            annotation["bbox"][0] + annotation["bbox"][2],
                            annotation["bbox"][1] + annotation["bbox"][3],
                        ],
                    ),
                    {
                        "category_id": annotation["category_id"],
                        "image_id": annotation["image_id"],
                    },
                )
            )
        annotations.append(image_annotations)
    return annotations


def convert_from_ground_truth_to_second_arg(dataset_annotations, dataset):
    """Convert ground truth annotations to COCOScorer format"""
    categories = {cat["id"]: cat["name"] for cat in dataset["categories"]}
    annotations = list()
    for dataset_image_annotations in dataset_annotations:
        image_annotations = list()
        for annotation in dataset_image_annotations:
            image_annotations.append(
                (
                    AxisAlignedBoundingBox(
                        annotation["bbox"][0:2],
                        [
                            annotation["bbox"][0] + annotation["bbox"][2],
                            annotation["bbox"][1] + annotation["bbox"][3],
                        ],
                    ),
                    {categories[annotation["category_id"]]: 1},
                )
            )
        annotations.append(image_annotations)
    return annotations


def convert_from_predictions_to_first_arg(predictions, dataset, ids):
    """Convert predictions to COCOScorer format"""
    predictions = convert_from_predictions_to_second_arg(predictions)
    categories = {cat["name"]: cat["id"] for cat in dataset["categories"]}
    real_ids = [id_.split("_")[-1] for id_ in ids]

    for id_, img_predictions in zip(real_ids, predictions):
        for prediction in img_predictions:
            class_name = list(prediction[1].keys())[0]

            prediction[1].clear()
            prediction[1]["image_id"] = int(id_)
            if class_name in categories:
                prediction[1]["category_id"] = categories[class_name]
            else:
                prediction[1]["category_id"] = 0

    return predictions


def convert_from_predictions_to_second_arg(predictions):
    """Convert predictions to COCOScorer format"""
    annotations_predictions = list()
    for img_predictions in predictions:
        current_annotations = list()
        for prediction in img_predictions[1]:
            if prediction:
                current_annotations.append(
                    (
                        AxisAlignedBoundingBox(
                            [prediction["box"]["xmin"], prediction["box"]["ymin"]],
                            [prediction["box"]["xmax"], prediction["box"]["ymax"]],
                        ),
                        {prediction["label"]: prediction["score"]},
                    )
                )

        annotations_predictions.append(current_annotations)

    return annotations_predictions


# Example usage:
# def is_odd(x):
#     return x % 2 == 1
# partition(is_odd, [1, 2, 3, 4])
def partition(pred, iterable):
    "Use a predicate to partition entries into false entries and true entries"
    # partition(is_odd, [1, 2, 3, 4]) --> ([2, 4], [1, 3])
    it = iter(iterable)
    true_result, false_result = [], []
    for elem in it:
        if pred(elem):
            true_result.append(elem)
        else:
            false_result.append(elem)
    return true_result, false_result


def compute_score(dataset_ids: Sequence[DatasetId], actual, predicted):
    """Compute score for image ids."""

    # separate images with no predictions in actual argument
    # as score function expects at least one prediction
    def is_empty(prediction_pair):
        actual_predictions = prediction_pair[0]
        return len(actual_predictions) == 0

    no_predictions, has_predictions = partition(is_empty, zip(actual, predicted, dataset_ids))

    both_images_no_prediction, one_has_prediction = partition(
        lambda pair: len(pair[1]) == 0, no_predictions
    )
    scores = []
    for _, __, dataset_id in both_images_no_prediction:
        scores.append((dataset_id, 1))
    for _, __, dataset_id in one_has_prediction:
        scores.append((dataset_id, 0))

    if len(has_predictions) == 0:
        return scores

    actual, predicted, dataset_ids = zip(*has_predictions)
    score_output = ClassAgnosticPixelwiseIoUScorer().score(actual, predicted)
    for dataset_id, score in zip(dataset_ids, score_output):
        scores.append((dataset_id, score))

    return scores
