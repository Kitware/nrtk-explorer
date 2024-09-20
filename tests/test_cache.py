import unittest
from unittest.mock import Mock

from nrtk_explorer.app.images.cache import LruCache


class TestLruCache(unittest.TestCase):

    def test_add_item(self):
        cache = LruCache(max_size=2)
        cache.add_item("key1", "value1")
        self.assertEqual(cache.get_item("key1"), "value1")

    def test_get_item(self):
        cache = LruCache(max_size=2)
        cache.add_item("key1", "value1")
        self.assertEqual(cache.get_item("key1"), "value1")
        self.assertIsNone(cache.get_item("key2"))

    def test_cache_max_size(self):
        cache = LruCache(max_size=2)
        cache.add_item("key1", "value1")
        cache.add_item("key2", "value2")
        cache.add_item("key3", "value3")
        self.assertIsNone(cache.get_item("key1"))
        self.assertEqual(cache.get_item("key2"), "value2")
        self.assertEqual(cache.get_item("key3"), "value3")

    def test_callbacks(self):
        cache = LruCache(max_size=2)
        on_add = Mock()
        on_clear = Mock()
        cache.add_item("key1", "value1", on_add_item=on_add, on_clear_item=on_clear)
        on_add.assert_called_once_with("key1", "value1")
        cache.clear()
        on_clear.assert_called_once_with("key1")

    def test_callback_called_once(self):
        cache = LruCache(max_size=2)
        on_add = Mock()
        on_clear = Mock()

        cache.add_item("key1", "value1", on_add_item=on_add, on_clear_item=on_clear)
        cache.add_item("key1", "value1", on_add_item=on_add, on_clear_item=on_clear)

        on_add.assert_called_once_with("key1", "value1")

        cache.clear()

        on_clear.assert_called_once_with("key1")

    def test_multiple_callbacks(self):
        cache = LruCache(max_size=2)
        on_add_1 = Mock()
        on_add_2 = Mock()
        on_clear_1 = Mock()
        on_clear_2 = Mock()

        cache.add_item("key1", "value1", on_add_item=on_add_1, on_clear_item=on_clear_1)
        cache.add_item("key1", "value1", on_add_item=on_add_2, on_clear_item=on_clear_2)

        on_add_1.assert_called_once_with("key1", "value1")
        on_add_2.assert_called_once_with("key1", "value1")

        cache.clear()

        on_clear_1.assert_called_once_with("key1")
        on_clear_2.assert_called_once_with("key1")


if __name__ == "__main__":
    unittest.main()
