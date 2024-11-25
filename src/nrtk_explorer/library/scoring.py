from typing import List, Dict, Tuple
from smqtk_image_io.bbox import AxisAlignedBoundingBox
from nrtk.impls.score_detections.class_agnostic_pixelwise_iou_scorer import (
    ClassAgnosticPixelwiseIoUScorer,
)


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
    return str(image_id).split("_")[-1]


def keys_to_dataset_ids(image_dict):
    """Convert keys to dataset ids."""
    return {image_id_to_dataset_id(key): value for key, value in image_dict.items()}


def get_cat_id(dataset, annotation):
    if "category_id" in annotation:
        return annotation["category_id"]
    cat = dataset.name_to_cat.get(annotation["label"], None)
    if not cat:
        return None
    return cat["id"]


def get_label(dataset, annotation):
    if annotation["category_id"] is not None:
        return dataset.cats[annotation["category_id"]]["name"]
    return annotation["label"]


def get_score(annotation):
    return 1.0 if "score" not in annotation else annotation["score"]


def normalize_annotation(dataset, image_id, annotation):
    """Normalize a single annotation."""
    category_id = get_cat_id(dataset, annotation)
    annotation = {
        **annotation,
        "category_id": category_id,
        "image_id": image_id,
        "score": get_score(annotation),
        "bbox": annotation.get("bbox", annotation.get("box", None)),
    }
    annotation["label"] = get_label(dataset, annotation)
    annotation[annotation["label"]] = annotation["score"]
    return annotation


def normalize_annotations(dataset, image_id, annotations):
    """Ensure category_id, bbox, label, score, [label]:score."""
    return [normalize_annotation(dataset, image_id, annotation) for annotation in annotations]


def predictions_to_annotations(dataset, ids, predictions):
    return [
        normalize_annotations(dataset, id, image_predictions)
        for id, image_predictions in zip(ids, predictions)
    ]


def get_category_similarity_score(actual: List[Dict], predicted: List[Dict]) -> float:
    """
    Calculate matching score between actual and predicted category annotations.

    Args:
        actual: List of actual annotation dictionaries with category_id
        predicted: List of predicted annotation dictionaries with category_id

    Returns:
        float: Matching score between 0.0 and 1.0
    """
    actual_cat_ids = set([annotation["category_id"] for annotation in actual])
    predicted_cat_ids = set([annotation["category_id"] for annotation in predicted])

    matching_cat_ids = sum(
        1 for cat_id in predicted_cat_ids if cat_id in actual_cat_ids and cat_id is not None
    )

    total_cat_ids = len(actual_cat_ids.union(predicted_cat_ids))
    return matching_cat_ids / total_cat_ids if total_cat_ids > 0 else 0.0


ImagePredictions = List[Dict]


def compute_category_similarity_scores(
    actual: List[ImagePredictions], predicted: List[ImagePredictions], ids: List[str]
) -> List[Tuple[str, float]]:
    """
    Calculate matching scores between actual and predicted category annotations.

    Args:
        actual: List of actual annotations
        predicted: List of predicted annotations
        ids: List of image IDs

    Returns:
        List of tuples containing (image_id, matching_score)
    """

    return [
        (id, get_category_similarity_score(actual, predicted))
        for actual, predicted, id in zip(actual, predicted, ids)
    ]


def get_aabb(annotation):
    bbox = annotation["bbox"]
    if "xmin" in bbox:
        return AxisAlignedBoundingBox(
            [bbox["xmin"], bbox["ymin"]],
            [bbox["xmax"], bbox["ymax"]],
        )
    return AxisAlignedBoundingBox(
        [bbox[0], bbox[1]],
        [bbox[0] + bbox[2], bbox[1] + bbox[3]],
    )


def to_nrtk_score_shape(annotation):
    return (
        get_aabb(annotation),
        annotation,
    )


def compute_score(dataset, actual, predicted):
    """Compute score for image ids."""

    actual = keys_to_dataset_ids(actual)
    predicted = keys_to_dataset_ids(predicted)
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

    actual = predictions_to_annotations(dataset, ids, actual)
    predicted = predictions_to_annotations(dataset, ids, predicted)

    all_annotations_have_bbox = all(
        annotation["bbox"] is not None
        for annotation_list in actual + predicted
        for annotation in annotation_list
    )

    if not all_annotations_have_bbox:
        s = compute_category_similarity_scores(actual, predicted, ids)
        return scores + s

    actual_converted = [
        [to_nrtk_score_shape(annotation) for annotation in img_annotations]
        for img_annotations in actual
    ]
    predicted_converted = [
        [to_nrtk_score_shape(annotation) for annotation in img_annotations]
        for img_annotations in predicted
    ]

    score_output = ClassAgnosticPixelwiseIoUScorer().score(actual_converted, predicted_converted)
    for id, score in zip(ids, score_output):
        scores.append((id, score))

    return scores
