from typing import Any, Callable, Dict, Sequence
from collections import OrderedDict
from PIL import Image
from trame.app import get_server
from nrtk_explorer.app.images.image_ids import (
    image_id_to_result_id,
    dataset_id_to_image_id,
    dataset_id_to_transformed_image_id,
)
from nrtk_explorer.app.images.image_meta import dataset_id_to_meta, update_image_meta
from nrtk_explorer.library.dataset import get_image_path
from nrtk_explorer.app.trame_utils import delete_state, change_checker
from nrtk_explorer.library.images_manager import convert_to_base64
from nrtk_explorer.library.object_detector import ObjectDetector
from nrtk_explorer.library.transforms import ImageTransform
from nrtk_explorer.library.coco_utils import partition


class BufferCache:
    """Least recently accessed item is removed when the cache is full."""

    def __init__(self, max_size: int, on_clear_item: Callable[[str], None]):
        self.cache: OrderedDict[str, Any] = OrderedDict()
        self.max_size = max_size
        self.on_clear_item = on_clear_item

    def add_item(self, key: str, item):
        """Add an item to the cache."""
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = item
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)

    def get_item(self, key: str):
        """Retrieve an item from the cache."""
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def clear_item(self, key: str):
        """Remove a specific item from the cache."""
        if key in self.cache:
            self.on_clear_item(key)
            del self.cache[key]

    def clear(self):
        """Clear the cache."""
        for key in self.cache.keys():
            self.on_clear_item(key)
        self.cache.clear()


server = get_server()
state, context, ctrl = server.state, server.context, server.controller


# syncs trame state
def delete_from_state(key: str):
    delete_state(state, key)


image_cache = BufferCache(100, delete_from_state)


def get_image(dataset_id: str):
    cached_image = image_cache.get_item(dataset_id)
    if cached_image is not None:
        return cached_image

    image_path = get_image_path(dataset_id)
    image = Image.open(image_path)

    image_cache.add_item(dataset_id, image)
    return image


def get_transformed_image(transform: ImageTransform, dataset_id: str):
    key = dataset_id_to_transformed_image_id(dataset_id)
    cached_image = image_cache.get_item(key)
    if cached_image is not None:
        return cached_image

    original = get_image(dataset_id)
    transformed = transform.execute(original)
    if original.size != transformed.size:
        # Resize so pixel-wise annotation similarity score works
        transformed = transformed.resize(original.size)

    image_cache.add_item(key, transformed)

    state[key] = convert_to_base64(transformed)

    return transformed


def add_annotation_to_state(image_id: str, annotations: Any):
    state[image_id_to_result_id(image_id)] = annotations


def delete_annotation_from_state(image_id: str):
    delete_state(state, image_id_to_result_id(image_id))


annotation_cache = BufferCache(1000, delete_annotation_from_state)


def prediction_to_annotations(predictions):
    annotations = []
    for prediction in predictions:
        category_id = None
        # if no matching category in dataset JSON, category_id will be None
        for cat_id, cat in state.annotation_categories.items():
            if cat["name"] == prediction["label"]:
                category_id = cat_id

        bbox = prediction["box"]
        annotations.append(
            {
                "category_id": category_id,
                "label": prediction["label"],
                "bbox": [
                    bbox["xmin"],
                    bbox["ymin"],
                    bbox["xmax"] - bbox["xmin"],
                    bbox["ymax"] - bbox["ymin"],
                ],
            }
        )
    return annotations


def get_annotations(detector: ObjectDetector, id_to_image: Dict[str, Image.Image]):
    hits, misses = partition(annotation_cache.get_item, id_to_image.keys())

    to_detect = {id: id_to_image[id] for id in misses}
    predictions = detector.eval(
        to_detect,
    )
    for id, annotations in predictions.items():
        annotation_cache.add_item(id, annotations)
        add_annotation_to_state(id, prediction_to_annotations(annotations))

    predictions.update(**{id: annotation_cache.get_item(id) for id in hits})
    # match input order because of scoring code assumptions
    return {id: predictions[id] for id in id_to_image.keys()}


def get_ground_truth_annotations(dataset_ids: Sequence[str]):
    hits, misses = partition(annotation_cache.get_item, dataset_ids)

    annotations = {
        dataset_id: [
            annotation
            for annotation in context.dataset.anns.values()
            if str(annotation["image_id"]) == dataset_id
        ]
        for dataset_id in misses
    }

    for id, boxes_for_image in annotations.items():
        annotation_cache.add_item(id, boxes_for_image)
        add_annotation_to_state(id, boxes_for_image)

    annotations.update({id: annotation_cache.get_item(id) for id in hits})
    return [annotations[dataset_id] for dataset_id in dataset_ids]


def get_image_state_keys(dataset_id: str):
    return {
        "ground_truth": image_id_to_result_id(dataset_id),
        "original_image_detection": image_id_to_result_id(dataset_id_to_image_id(dataset_id)),
        "transformed_image": dataset_id_to_transformed_image_id(dataset_id),
        "transformed_image_detection": image_id_to_result_id(
            dataset_id_to_transformed_image_id(dataset_id)
        ),
        "meta_id": dataset_id_to_meta(dataset_id),
    }


@state.change("current_dataset")
def clear_all(**kwargs):
    image_cache.clear()
    annotation_cache.clear()


@change_checker(state, "dataset_ids")
def init_state(old, new):
    if old is not None:
        # clean old ids that are not in new
        old_ids = set(old)
        new_ids = set(new)
        to_clean = old_ids - new_ids
        for id in to_clean:
            image_cache.clear_item(id)  # original image
            annotation_cache.clear_item(id)  # ground truth
            annotation_cache.clear_item(dataset_id_to_image_id(id))  # original image detection
            keys = get_image_state_keys(id)
            image_cache.clear_item(keys["transformed_image"])
            annotation_cache.clear_item(keys["transformed_image"])
            for key in keys.values():
                delete_state(state, key)

    # create reactive annotation variables so ImageDetection component has live Refs
    for id in new:
        keys = get_image_state_keys(id)
        for key in keys.values():
            if not state.has(key):
                state[key] = None
    state.hovered_id = None


def clear_transformed(**kwargs):
    for id in state.dataset_ids:
        keys = get_image_state_keys(id)
        image_cache.clear_item(keys["transformed_image"])
        annotation_cache.clear_item(keys["transformed_image"])
        update_image_meta(
            state,
            id,
            {
                "original_detection_to_transformed_detection_score": 0,
                "ground_truth_to_transformed_detection_score": 0,
            },
        )


ctrl.apply_transform.add(clear_transformed)
