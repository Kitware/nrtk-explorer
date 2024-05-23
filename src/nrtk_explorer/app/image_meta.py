from typing import TypedDict

DatasetId = str


def image_id_to_meta(image_id: DatasetId):
    return f"{image_id}_meta"


class DatasetImageMeta(TypedDict):
    width: int
    height: int


PartialDatasetImageMeta = TypedDict(
    "PartialDatasetImageMeta", {**DatasetImageMeta.__annotations__}, total=False
)

IMAGE_META_DEFAULTS: DatasetImageMeta = {"width": 0, "height": 0}


def update_image_meta(state, dataset_id: DatasetId, meta: PartialDatasetImageMeta):
    meta_key = image_id_to_meta(dataset_id)
    current_meta = {}
    if state.has(meta_key) and state[meta_key] is not None:
        current_meta = state[meta_key]
    state[meta_key] = {**IMAGE_META_DEFAULTS, **current_meta, **meta}


def delete_image_meta(state, dataset_id: DatasetId):
    meta_key = image_id_to_meta(dataset_id)
    if state.has(meta_key):
        state[meta_key] = None
