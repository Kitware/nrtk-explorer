from smqtk_image_io.bbox import AxisAlignedBoundingBox
from nrtk.impls.score_detections.class_agnostic_pixelwise_iou_scorer import (
    ClassAgnosticPixelwiseIoUScorer,
)

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
    categories = {cat["id"]: cat["name"] for cat in dataset.cats.values()}
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
    categories = {cat["name"]: cat["id"] for cat in dataset.cats.values()}
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
        for prediction in img_predictions:
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
# partition(is_odd, [1, 2, 3, 4]) --> ([1, 3], [2, 4])
def partition(pred, iterable):
    "Use a predicate to partition entries into true entries and false entries"
    it = iter(iterable)
    true_result, false_result = [], []
    for elem in it:
        if pred(elem):
            true_result.append(elem)
        else:
            false_result.append(elem)
    return true_result, false_result


def image_id_to_dataset_id(image_id):
    return image_id.split("_")[-1]


def keys_to_dataset_ids(image_dict):
    """Convert keys to dataset ids."""
    return {image_id_to_dataset_id(key): value for key, value in image_dict.items()}


def compute_score(dataset, actual_info, predicted_info):
    """Compute score for image ids."""

    actual = keys_to_dataset_ids(actual_info["annotations"])
    predicted = keys_to_dataset_ids(predicted_info["annotations"])
    ids = list(actual.keys())

    pairs = [(actual[key], predicted[key], key) for key in ids]

    # separate images with no predictions in actual argument
    # as score function expects at least one prediction
    def is_empty(prediction_pair):
        actual_predictions = prediction_pair[0]
        return len(actual_predictions) == 0

    no_annotations, has_annotations = partition(is_empty, pairs)

    both_images_no_annotation, one_has_annotation = partition(
        lambda pair: len(pair[1]) == 0, no_annotations
    )
    scores = []
    for _, __, id in both_images_no_annotation:
        scores.append((id, 1.0))
    for _, __, id in one_has_annotation:
        scores.append((id, 0.0))

    if len(has_annotations) == 0:
        return scores

    actual, predicted, ids = zip(*has_annotations)

    if actual_info["type"] == "predictions":
        actual_converted = convert_from_predictions_to_first_arg(
            actual,
            dataset,
            ids,
        )
    elif actual_info["type"] == "truth":
        actual_converted = convert_from_ground_truth_to_first_arg(actual)

    if predicted_info["type"] == "predictions":
        predicted_converted = convert_from_predictions_to_second_arg(
            predicted,
        )
    elif predicted_info["type"] == "truth":
        predicted_converted = convert_from_ground_truth_to_second_arg(predicted, dataset)

    score_output = ClassAgnosticPixelwiseIoUScorer().score(actual_converted, predicted_converted)
    for id, score in zip(ids, score_output):
        scores.append((id, score))

    return scores
