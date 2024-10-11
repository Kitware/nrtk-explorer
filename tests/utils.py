import json
import os
from PIL import Image
import nrtk_explorer.test_data

DIR_PATH = os.path.dirname(nrtk_explorer.test_data.__file__)
DATASET_PATH = f"{DIR_PATH}/coco-od-2017/"
DATASET = f"{DATASET_PATH}/test_val2017.json"


def get_images():
    ds = json.load(open(DATASET))
    return {img["id"]: Image.open(f"{DATASET_PATH}/{img['file_name']}") for img in ds["images"]}


def get_image():
    ds = json.load(open(DATASET))
    return Image.open(f"{DATASET_PATH}/{ds['images'][0]['file_name']}")
