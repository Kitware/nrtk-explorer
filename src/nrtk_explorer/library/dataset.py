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


def loadDataset(path: str) -> Dataset:
    with open(path) as f:
        return json.load(f)


datasetJson: Dataset = {"categories": [], "images": [], "annotations": []}
_datasetPath: str = ""


def getDataset(path: str) -> Dataset:
    global datasetJson, _datasetPath
    if _datasetPath != path:
        _datasetPath = path
        datasetJson = loadDataset(_datasetPath)
    return datasetJson
