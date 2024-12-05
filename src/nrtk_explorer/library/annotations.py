from typing import TypedDict, List
from .dataset import JsonDataset


def get_cat_id(dataset, annotation):
    if "category_id" in annotation:
        return annotation["category_id"]
    cat = dataset.name_to_cat.get(annotation["label"], None)
    if not cat:
        return None
    return cat["id"]


class PredictionBox(TypedDict):
    xmin: float
    ymin: float
    xmax: float
    ymax: float


# from hugging face transformers.pipeline output
class Prediction(TypedDict, total=False):
    label: str
    score: float
    box: PredictionBox


# COCO dataset annotation plus maybe score
class Annotation(TypedDict, total=False):
    category_id: int
    label: str
    score: float
    bbox: List[float]


def to_annotation(dataset: JsonDataset, prediction: Prediction) -> Annotation:
    annotation: Annotation = {}

    if "label" in prediction:
        annotation["label"] = prediction["label"]
        annotation["category_id"] = get_cat_id(dataset, annotation)

    if "score" in prediction:
        annotation["score"] = prediction["score"]

    if "box" in prediction:
        bbox = prediction["box"]
        annotation["bbox"] = [
            bbox["xmin"],
            bbox["ymin"],
            bbox["xmax"] - bbox["xmin"],
            bbox["ymax"] - bbox["ymin"],
        ]

    return annotation
