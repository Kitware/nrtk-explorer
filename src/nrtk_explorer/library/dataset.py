"""
Module to load a dataset.

Example:
    dataset = get_dataset("path/to/dataset.json")
"""

from typing import Sequence as SequenceType
from functools import lru_cache
from pathlib import Path
import json
from PIL import Image
from datasets import (
    load_dataset,
    get_dataset_infos,
    Sequence,
    ClassLabel,
)


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


def expand_hugging_face_datasets(dataset_identifiers: SequenceType[str]):
    expanded_identifiers = []
    for identifier in dataset_identifiers:
        if is_coco_dataset(identifier):
            expanded_identifiers.append(identifier)
        else:
            infos = get_dataset_infos(identifier)
            for config_name, info in infos.items():
                for split_name in info.splits:
                    expanded_identifiers.append(f"{identifier}@{config_name}@{split_name}")
    return expanded_identifiers


HF_ROWS_MAX_TO_DOWNLOAD = 5000
HF_ROWS_TO_TAKE_STREAMING = 1000


class HuggingFaceDataset:
    """Interface to Hugging Face Dataset with the same API as JsonDataset."""

    def __init__(self, identifier: str):
        parts = identifier.split("@")
        if len(parts) == 3:
            repo_name, selected_config_name, selected_split_name = parts
        else:
            raise ValueError("Identifier must be in the format 'dataset@config@split'")

        infos = get_dataset_infos(repo_name)
        selected_info = infos[selected_config_name]
        num_examples = selected_info.splits[selected_split_name].num_examples
        self._streaming = num_examples > HF_ROWS_MAX_TO_DOWNLOAD

        dataset = load_dataset(
            repo_name, selected_config_name, split=selected_split_name, streaming=self._streaming
        )

        if self._streaming:
            self._dataset = dataset.take(HF_ROWS_TO_TAKE_STREAMING)
        else:
            self._dataset = dataset
        self._metadata = self._dataset.remove_columns(["image"])

        imgs, row_idx_to_id, id_to_row_idx = self._load_images()
        self.imgs = imgs
        self._row_idx_to_id = row_idx_to_id
        self._id_to_row_idx = id_to_row_idx

        self.cats = self._load_categories()

        self.anns = self._load_annotations()

    def _load_images(self):
        images = {}
        row_idx_to_id = {}
        id_to_row_idx = {}
        dataset = self._dataset if self._streaming else self._metadata
        for idx, example in enumerate(dataset):
            id = example.get("id", example.get("image_id", idx))
            images[id] = {
                "id": id,
            }
            row_idx_to_id[idx] = id
            id_to_row_idx[id] = example["image"] if self._streaming else idx

        return images, row_idx_to_id, id_to_row_idx

    def get_image(self, id):
        """Get the image given an image id."""
        if self._streaming:
            return self._id_to_row_idx[id]
        row = self._id_to_row_idx[id]
        return self._dataset[row]["image"]

    def _load_categories(self):
        labels = None
        if "labels" in self._metadata.features:
            labels = self._metadata.features["labels"].names

        if "objects" in self._metadata.features:
            objects = self._metadata.features["objects"]

            if not isinstance(objects, Sequence) and "category" in objects:
                category_feature = objects["category"]
                if isinstance(category_feature, Sequence):
                    if hasattr(category_feature.feature, "names"):
                        labels = category_feature.feature.names
                    else:
                        # Try to get unique categories from the dataset
                        categories = set()
                        for example in self._metadata:
                            if "objects" in example and "category" in example["objects"]:
                                categories.update(example["objects"]["category"])
                        labels = sorted(list(categories))
                elif isinstance(category_feature, ClassLabel):
                    labels = category_feature.names
                elif hasattr(category_feature, "names"):
                    labels = category_feature.names
            else:
                category_feature = self._metadata.features["objects"].feature["category"]
                if hasattr(category_feature, "names"):
                    labels = category_feature.names
                else:
                    # Fallback to collecting unique categories
                    categories = set()
                    for example in self._metadata:
                        if "objects" in example:
                            categories.update(example["objects"]["category"])
                    labels = sorted(list(categories))

        if labels is None:
            print("Could not find category labels in dataset")
            return {}

        return {i: {"id": i, "name": str(name)} for i, name in enumerate(labels)}

    def _load_annotations(self):
        annotations = {}

        counter = 0

        def make_id():
            nonlocal counter
            counter += 1
            return f"ann_{counter}"

        for idx, example in enumerate(self._metadata):
            if "objects" in example:
                objects = example["objects"]
                image_id = self._row_idx_to_id[idx]
                dataset_has_ids = True
                ids = objects.get("id", objects.get("bbox_id"))
                if ids is None:
                    ids = [make_id() for _ in range(len(objects["bbox"]))]
                    dataset_has_ids = False

                for annotation_id, bbox, category_id in zip(
                    ids, objects["bbox"], objects["category"]
                ):
                    if category_id not in self.cats:
                        # assuming category_id is the name, find the id
                        category_name = category_id
                        category_id = next(
                            (
                                cat_id
                                for cat_id, cat in self.cats.items()
                                if cat["name"] == category_name
                            ),
                            None,
                        )

                    annotations[annotation_id] = {
                        "id": annotation_id if dataset_has_ids else None,
                        "image_id": image_id,
                        "category_id": category_id,
                        "bbox": bbox,
                    }

        # for idx, example in enumerate(self._metadata):
        #     if "labels" in example:
        #         image_id = self._row_idx_to_id[idx]
        #         image = example["image"]
        #         annotation_id = make_id()
        #         annotations[annotation_id] = {
        #             "id": None,
        #             "image_id": image_id,
        #             "category_id": example["labels"],
        #             "bbox": [2, 2, image.width - 2, image.height - 2],
        #         }

        return annotations


@lru_cache
def __load_dataset(identifier: str):
    """Load the dataset."""

    absolute_path = str(Path(identifier).resolve())

    if is_coco_dataset(absolute_path):
        return make_coco_dataset(absolute_path)

    # Assume identifier is a Hugging Face Dataset
    return HuggingFaceDataset(identifier)


def get_dataset(identifier: str):
    """Get the dataset object.
    Args:
        identifier (str): Path to the dataset file or HuggingFace hub dataset identifier.
    Return:
        dataset: Dataset object.
    """
    return __load_dataset(identifier)
