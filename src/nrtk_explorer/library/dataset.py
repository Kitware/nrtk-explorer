import kwcoco


def load_dataset(path: str):
    return kwcoco.CocoDataset(path)


dataset_json: kwcoco.CocoDataset = kwcoco.CocoDataset()
dataset_path: str = ""


def get_dataset(path: str, force_reload=False):
    global dataset_json, dataset_path
    if dataset_path != path or force_reload:
        dataset_path = path
        dataset_json = load_dataset(dataset_path)
    return dataset_json
