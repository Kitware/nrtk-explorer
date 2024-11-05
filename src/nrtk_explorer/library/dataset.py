"""
Module to load a dataset.

Example:
    dataset = get_dataset("path/to/dataset.json")
"""

from functools import lru_cache
from pathlib import Path
import json
from PIL import Image


class JsonDataset:
    """Read a COCO JSON and get the image file path given an image id."""

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

    def get_image(self, id: int):
        """Get the image given an image id."""
        image_fpath = self.get_image_fpath(id)
        return Image.open(image_fpath)


def make_coco_dataset(path: str):
    try:
        import kwcoco

        class NrtkCocoDataset(kwcoco.CocoDataset):
            def get_image(self, id: int):
                """Get the image given an image id."""
                image_fpath = self.get_image_fpath(id)
                return Image.open(image_fpath)

        return NrtkCocoDataset(path)
    except ImportError:
        return JsonDataset(path)


def is_coco_dataset(path: str):
    """Check if the file is a COCO dataset JSON."""
    import os

    if not os.path.exists(path):
        return False

    required_keys = ['"images"', '"categories"', '"annotations"']
    with open(path) as f:
        content = f.read()
        return all(key in content for key in required_keys)


class HuggingFaceDataset:
    """Interface to Hugging Face Dataset with the same API as JsonDataset."""

    def __init__(self, identifier: str):
        from datasets import load_dataset, get_dataset_default_config_name, get_dataset_infos

        infos = get_dataset_infos(identifier)
        selected_split_name = None
        selected_config_name = get_dataset_default_config_name(identifier)
        if selected_config_name is None:
            max_rows = 0
            for config_name, info in infos.items():
                for split_name, split_info in info.splits.items():
                    if split_info.num_examples > max_rows:
                        max_rows = split_info.num_examples
                        selected_config_name = config_name
                        selected_split_name = split_name
        if selected_split_name is None:
            split_infos = infos[selected_config_name].splits
            selected_split_name, _ = max(
                split_infos.items(),
                key=lambda item: item[1].num_examples,
            )

        self.dataset = load_dataset(identifier, selected_config_name, split=selected_split_name)
        self.cats = self._load_categories()
        self.anns = self._load_annotations()
        self.imgs = self._load_images()

    def _load_categories(self):
        if "labels" in self.dataset.features:
            labels = self.dataset.features["labels"].names
            return {i: {"id": i, "name": name} for i, name in enumerate(labels)}

        if "objects" in self.dataset.features:
            labels = self.dataset.features["objects"].feature["category"].names
            return {i: {"id": i, "name": name} for i, name in enumerate(labels)}
        return {}

    def _load_annotations(self):
        annotations = {}
        for idx, example in enumerate(self.dataset):
            if "objects" in example:
                objects = example["objects"]
                image_id = example.get("id", idx)
                id_key = "id" if "id" in objects else "bbox_id"
                for obj_id, bbox, category_id in zip(
                    objects[id_key], objects["bbox"], objects["category"]
                ):
                    annotations[obj_id] = {
                        "id": obj_id,
                        "image_id": image_id,
                        "category_id": category_id,
                        "bbox": bbox,
                    }

        counter = 1

        def get_id(annotations):
            nonlocal counter
            """Generate a unique string ID not present in annotations."""
            while True:
                new_id = f"ann_{counter}"
                if new_id not in annotations:
                    return new_id
                counter += 1

        for idx, example in enumerate(self.dataset):
            if "labels" in example:
                image = example["image"]
                annotation_id = get_id(annotations)
                annotations[annotation_id] = {
                    "id": annotation_id,
                    "image_id": idx,
                    "category_id": example["labels"],
                    "bbox": [2, 2, image.width - 2, image.height - 2],
                }

        return annotations

    def _load_images(self):
        images = {}
        for idx, example in enumerate(self.dataset):
            image = example["image"]
            id = example.get("id", idx)
            images[id] = {
                "id": id,
                "height": image.height,
                "width": image.width,
            }
        return images

    def get_image_fpath(self, selected_id: int):
        """Get the image file path given an image id."""
        image = self.imgs.get(selected_id)
        if image:
            return image["file_name"]
        raise KeyError(f"Image ID {selected_id} not found.")

    def get_image(self, id: int):
        """Get the image given an image id."""
        return self.dataset[id]["image"]


def wrap_hugging_face_dataset(identifier):
    return HuggingFaceDataset(identifier)


@lru_cache
def __load_dataset(identifier: str):
    """Load the dataset given the path to the dataset file."""

    absolute_path = str(Path(identifier).resolve())

    if is_coco_dataset(absolute_path):
        return make_coco_dataset(absolute_path)

    # Assume identifier is a Hugging Face Dataset
    return wrap_hugging_face_dataset(identifier)


def get_dataset(identifier: str, force_reload: bool = False):
    """Get the dataset object given the path to the dataset file.
    Args:
        path (str): Path to the dataset file.
        force_reload (bool): Whether to force reload the dataset. Default: False.
    Return:
        dataset: Dataset object.
    """
    if force_reload:
        __load_dataset.cache_clear()
    return __load_dataset(identifier)


def get_image_fpath(selected_id: int, path: str):
    """Get the image file path given an image id."""
    return get_dataset(path).get_image_fpath(selected_id)
