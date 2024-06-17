from typing import TypedDict
from nrtk_explorer.app.trame_utils import delete_state
from nrtk_explorer.app.image_ids import DatasetId

ImageMetaId = str


def image_id_to_meta(image_id: DatasetId) -> ImageMetaId:
    return f"meta_{image_id}"


class DatasetImageMeta(TypedDict):
    original_ground_to_original_detection_score: float
    original_detection_to_transformed_detection_score: float
    ground_truth_to_transformed_detection_score: float


PartialDatasetImageMeta = TypedDict(
    "PartialDatasetImageMeta", {**DatasetImageMeta.__annotations__}, total=False
)

IMAGE_META_DEFAULTS: DatasetImageMeta = {
    "original_ground_to_original_detection_score": 0,
    "original_detection_to_transformed_detection_score": 0,
    "ground_truth_to_transformed_detection_score": 0,
}


def update_image_meta(state, dataset_id: DatasetId, meta_patch: PartialDatasetImageMeta):
    meta_key = image_id_to_meta(dataset_id)
    current_meta = {}
    if state.has(meta_key) and state[meta_key] is not None:
        current_meta = state[meta_key]
    state[meta_key] = {**IMAGE_META_DEFAULTS, **current_meta, **meta_patch}


def delete_image_meta(state, dataset_id: DatasetId):
    meta_key = image_id_to_meta(dataset_id)
    delete_state(state, meta_key)
