from typing import Union

DatasetId = str
SourceImageId = str
TransformedImageId = str
ImageId = Union[SourceImageId, TransformedImageId]
ResultId = str


def image_id_to_dataset_id(image_id: ImageId) -> DatasetId:
    return image_id.split("_")[-1]


def image_id_to_result_id(image_id: ImageId) -> ResultId:
    return f"result_{image_id}"
