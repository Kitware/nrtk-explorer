from typing import Any, Callable, Dict, Sequence
from collections import OrderedDict
from functools import lru_cache, partial
from PIL import Image
from nrtk_explorer.library.object_detector import ObjectDetector
from nrtk_explorer.library.coco_utils import partition


ANNOTATION_CACHE_SIZE = 500


class DeleteCallbackRef:
    def __init__(self, del_callback, value):
        self.del_callback = del_callback
        self.value = value

    def __del__(self):
        self.del_callback()


def get_annotations_from_dataset(
    context, add_to_cache_callback, delete_from_cache_callback, dataset_id: str
):
    dataset = context.dataset
    annotations = [
        annotation
        for annotation in dataset.anns.values()
        if str(annotation["image_id"]) == dataset_id
    ]
    add_to_cache_callback(dataset_id, annotations)
    with_id = partial(delete_from_cache_callback, dataset_id)
    return DeleteCallbackRef(with_id, annotations)


class GroundTruthAnnotations:
    def __init__(
        self,
        context,  # for dataset
        add_to_cache_callback,
        delete_from_cache_callback,
    ):
        with_callbacks = partial(
            get_annotations_from_dataset,
            context,
            add_to_cache_callback,
            delete_from_cache_callback,
        )
        self.get_annotations_for_image = lru_cache(maxsize=ANNOTATION_CACHE_SIZE)(with_callbacks)

    def get_annotations(self, dataset_ids: Sequence[str]):
        return {
            dataset_id: self.get_annotations_for_image(dataset_id).value
            for dataset_id in dataset_ids
        }

    def cache_clear(self):
        self.get_annotations_for_image.cache_clear()


class LruCache:
    """Least recently accessed item is removed when the cache is full."""

    def __init__(
        self,
        max_size: int,
        on_add_item: Callable[[str, Any], None],
        on_clear_item: Callable[[str], None],
    ):
        self.cache: OrderedDict[str, Any] = OrderedDict()
        self.max_size = max_size
        self.on_add_item = on_add_item
        self.on_clear_item = on_clear_item

    def add_item(self, key: str, item):
        """Add an item to the cache."""
        self.cache[key] = item
        self.cache.move_to_end(key)
        if len(self.cache) > self.max_size:
            oldest = next(iter(self.cache))
            self.clear_item(oldest)
        self.on_add_item(key, item)

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


class DetectionAnnotations:
    def __init__(
        self,
        add_to_cache_callback,
        delete_from_cache_callback,
    ):
        self.cache = LruCache(
            ANNOTATION_CACHE_SIZE, add_to_cache_callback, delete_from_cache_callback
        )

    def get_annotations(self, detector: ObjectDetector, id_to_image: Dict[str, Image.Image]):
        hits, misses = partition(self.cache.get_item, id_to_image.keys())
        cached_predictions = {id: self.cache.get_item(id) for id in hits}

        to_detect = {id: id_to_image[id] for id in misses}
        predictions = detector.eval(
            to_detect,
        )
        for id, annotations in predictions.items():
            self.cache.add_item(id, annotations)

        predictions.update(**cached_predictions)
        # match input order because of scoring code assumptions
        return {id: predictions[id] for id in id_to_image.keys()}

    def cache_clear(self):
        self.cache.clear()
