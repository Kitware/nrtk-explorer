from typing import TypedDict, List
import json


class DatasetCategory(TypedDict):
    id: int
    name: str


class DatasetImage(TypedDict):
    id: int
    file_name: str
    width: int
    height: int


class DatasetAnnotation(TypedDict):
    id: int
    image_id: int
    category_id: int
    bbox: List[int]


class Dataset(TypedDict):
    categories: List[DatasetCategory]
    images: List[DatasetImage]
    annotations: List[DatasetAnnotation]


def load_dataset(path: str) -> Dataset:
    with open(path) as f:
        return json.load(f)


dataset_json: Dataset = {"categories": [], "images": [], "annotations": []}
dataset_path: str = ""


def get_dataset(path: str) -> Dataset:
    global dataset_json, dataset_path
    if dataset_path != path:
        dataset_path = path
        dataset_json = load_dataset(dataset_path)
    return dataset_json
