from typing import Any, Callable, List, NamedTuple
from collections import OrderedDict

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

    def _cache_full(self):
        return len(self.cache) >= self.max_size

    def add_item(
        self,
        key: str,
        item: Item,
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
            self._clear_item(key)
            cache_item = None

        if self._cache_full():
            oldest = next(iter(self.cache))
            self._clear_item(oldest)

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

    def add_if_room(self, key: str, item: Item, **kwargs):
        """Does not remove items from cache, only adds."""
        if not self._cache_full():
            self.add_item(key, item, **kwargs)

    def get_item(self, key: str):
        """Retrieve an item from the cache."""
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key].item
        return None

    def _clear_item(self, key: str):
        """Remove a specific item from the cache."""
        if key in self.cache:
            for callback in self.cache[key].on_clear_item_callbacks:
                callback(key)
            del self.cache[key]

    def clear(self):
        """Clear the cache."""
        for key in list(self.cache.keys()):
            self._clear_item(key)
