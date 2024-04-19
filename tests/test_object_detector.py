from nrtk_explorer.library import object_detector

import json
import os
import nrtk_explorer.test_data

DIR_PATH = os.path.dirname(nrtk_explorer.test_data.__file__)
DATASET_PATH = f"{DIR_PATH}/coco-od-2017/"
DATASET = f"{DATASET_PATH}/test_val2017.json"


def test_detector_small():
    ds = json.load(open(DATASET))
    sample = [f"{DATASET_PATH}/{img['file_name']}" for img in ds["images"]][:15]
    detector = object_detector.ObjectDetector(model_name="hustvl/yolos-tiny")
    img = detector.eval(paths=sample)
    assert len(img) == 15
