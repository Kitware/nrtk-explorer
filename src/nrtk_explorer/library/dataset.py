"""
Module to load the dataset and get the image file path given an image id.

Example:
    dataset = get_dataset("path/to/dataset.json")
    image_fpath = dataset.get_image_fpath(image_id)
"""

from functools import lru_cache
from pathlib import Path

import json


class DefaultDataset:
    """Default dataset class to load the dataset and get the image file path given an image id."""

    def __init__(self, path: str):
        with open(path) as f:
            self.data = json.load(f)
            self.fpath = path
            self.cats = {cat["id"]: cat for cat in self.data["categories"]}
            self.anns = {ann["id"]: ann for ann in self.data["annotations"]}
            self.imgs = {img["id"]: img for img in self.data["images"]}

    def get_image_fpath(self, selected_id: int):
        """Get the image file path given an image id."""
        dataset_dir = Path(self.fpath).parent
        file_name = self.imgs[selected_id]["file_name"]
        return str(dataset_dir / file_name)


@lru_cache
def __load_dataset(path: str):
    """Load the dataset given the path to the dataset file."""
    try:
        import kwcoco

        return kwcoco.CocoDataset(path)
    except ImportError:
        return DefaultDataset(path)


def get_dataset(path: str, force_reload: bool = False):
    """Get the dataset object given the path to the dataset file.
    Args:
        path (str): Path to the dataset file.
        force_reload (bool): Whether to force reload the dataset. Default: False.
    Return:
        dataset: Dataset object.
    """
    if force_reload:
        __load_dataset.cache_clear()
    return __load_dataset(path)


def get_image_fpath(selected_id: int, path: str):
    """Get the image file path given an image id."""
    return get_dataset(path).get_image_fpath(selected_id)
