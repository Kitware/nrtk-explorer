from typing import Any, Callable, List, NamedTuple
from collections import OrderedDict
import base64
import io
from PIL import Image
from trame.decorators import TrameApp, change, controller
from nrtk_explorer.app.images.image_ids import (
    dataset_id_to_image_id,
    dataset_id_to_transformed_image_id,
)
from nrtk_explorer.app.trame_utils import delete_state
from nrtk_explorer.library.transforms import ImageTransform


def convert_to_base64(img: Image.Image) -> str:
    """Convert image to base64 string"""
    buf = io.BytesIO()
    img.save(buf, format="png")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


IMAGE_CACHE_SIZE = 200

Item = Any


class CacheItem(NamedTuple):
    item: Item
    on_add_item_callbacks: List[Callable[[str, Item], None]]
    on_clear_item_callbacks: List[Callable[[str], None]]


def noop(*args, **kwargs):
    pass


class LruCache:
    """
    Least recently accessed item is removed when the cache is full.
    Per item callbacks are called when an item is added or cleared.
    Useful for side effects like updating the trame state.
    """

    def __init__(self, max_size: int):
        self.cache: OrderedDict[str, CacheItem] = OrderedDict()
        self.max_size = max_size

    def cache_full(self):
        return len(self.cache) >= self.max_size

    def add_item(
        self,
        key: str,
        item,
        on_add_item: Callable[[str, Any], None] = noop,
        on_clear_item: Callable[[str], None] = noop,
    ):
        """
        Add an item to the cache.
        Runs on_add_item callback if callback does not exist in current item callbacks list or item is new
        """
        cache_item = self.cache.get(key)
        if cache_item and cache_item.item != item:
            # stale cached item, clear it
            self.clear_item(key)
            cache_item = None

        if self.cache_full():
            oldest = next(iter(self.cache))
            self.clear_item(oldest)

        if cache_item:
            # Update callbacks list only if they are not already present
            if on_add_item not in cache_item.on_add_item_callbacks:
                cache_item.on_add_item_callbacks.append(on_add_item)
                on_add_item(key, item)
            if on_clear_item not in cache_item.on_clear_item_callbacks:
                cache_item.on_clear_item_callbacks.append(on_clear_item)
        else:
            # Create a new CacheItem and add it to the cache
            cache_item = CacheItem(
                item=item,
                on_add_item_callbacks=[on_add_item],
                on_clear_item_callbacks=[on_clear_item],
            )
            self.cache[key] = cache_item
            on_add_item(key, item)

        self.cache.move_to_end(key)

    def clear_item(self, key: str):
        """Remove a specific item from the cache."""
        if key in self.cache:
            for callback in self.cache[key].on_clear_item_callbacks:
                callback(key)
            del self.cache[key]

    def get_item(self, key: str):
        """Retrieve an item from the cache."""
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key].item
        return None

    def clear(self):
        """Clear the cache."""
        for key in list(self.cache.keys()):
            self.clear_item(key)


@TrameApp()
class Images:
    def __init__(self, server):
        self.server = server
        self.original_images = LruCache(
            IMAGE_CACHE_SIZE,
        )
        self.transformed_images = LruCache(
            IMAGE_CACHE_SIZE,
        )

    def _load_image(self, dataset_id: str):
        image_path = self.server.controller.get_image_fpath(int(dataset_id))
        return Image.open(image_path)

    def get_image(self, dataset_id: str, **kwargs):
        image_id = dataset_id_to_image_id(dataset_id)
        image = self.original_images.get_item(image_id) or self._load_image(dataset_id)
        self.original_images.add_item(image_id, image, **kwargs)
        return image

    def get_stateful_image(self, dataset_id: str):
        return self.get_image(
            dataset_id, on_add_item=self._add_image_to_state, on_clear_item=self._delete_from_state
        )

    def _add_image_to_state(self, image_id: str, image: Image.Image):
        self.server.state[image_id] = convert_to_base64(image)

    def _delete_from_state(self, state_key: str):
        delete_state(self.server.state, state_key)

    def get_image_without_cache_eviction(self, dataset_id: str):
        image_id = dataset_id_to_image_id(dataset_id)
        image = self.original_images.get_item(image_id)
        if not image:
            image = self._load_image(dataset_id)
        if not self.original_images.cache_full():
            self.original_images.add_item(image_id, image)
        return image

    def _load_transformed_image(self, transform: ImageTransform, dataset_id: str):
        original = self.get_image_without_cache_eviction(dataset_id)
        transformed = transform.execute(original)
        # So pixel-wise annotation similarity score works
        if original.size != transformed.size:
            return transformed.resize(original.size)
        return transformed

    def get_transformed_image(self, transform: ImageTransform, dataset_id: str, **kwargs):
        image_id = dataset_id_to_transformed_image_id(dataset_id)
        image = self.transformed_images.get_item(image_id) or self._load_transformed_image(
            transform, dataset_id
        )
        self.transformed_images.add_item(image_id, image, **kwargs)
        return image

    def get_stateful_transformed_image(self, transform: ImageTransform, dataset_id: str):
        return self.get_transformed_image(
            transform,
            dataset_id,
            on_add_item=self._add_image_to_state,
            on_clear_item=self._delete_from_state,
        )

    @change("current_dataset")
    def clear_all(self, **kwargs):
        self.original_images.clear()
        self.clear_transformed()

    @controller.add("apply_transform")
    def clear_transformed(self, **kwargs):
        self.transformed_images.clear()
