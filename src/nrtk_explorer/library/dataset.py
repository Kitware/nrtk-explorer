from typing import TypedDict, List


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
