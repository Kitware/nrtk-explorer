import kwcoco
from pathlib import Path


def load_dataset(path: str):
    return kwcoco.CocoDataset(path)


dataset: kwcoco.CocoDataset = kwcoco.CocoDataset()
dataset_path: str = ""


def get_dataset(path: str, force_reload=False):
    global dataset, dataset_path
    if dataset_path != path or force_reload:
        dataset_path = path
        dataset = load_dataset(dataset_path)
    return dataset


def get_image_path(id: str):
    dataset_dir = Path(dataset_path).parent
    file_name = dataset.imgs[int(id)]["file_name"]
    return str(dataset_dir / file_name)
