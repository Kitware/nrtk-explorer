from nrtk_explorer.library import object_detector
from nrtk_explorer.library.scoring import compute_score
from nrtk_explorer.library.dataset import get_dataset
from utils import get_images, DATASET


def test_detector_small():
    sample = get_images()
    detector = object_detector.ObjectDetector(model_name="hustvl/yolos-tiny")
    img = detector.eval(sample)
    assert len(img) == len(sample.keys())


def test_scorer():
    ds = get_dataset(DATASET)
    sample = get_images()
    detector = object_detector.ObjectDetector(model_name="facebook/detr-resnet-50")
    predictions = detector.eval(sample)

    dataset_annotations = dict()
    for annotation in ds.anns.values():
        image_annotations = dataset_annotations.setdefault(annotation["image_id"], [])
        image_annotations.append(annotation)

    ground_truth_annotations = dict()
    for img in ds.imgs.values():
        ground_truth_annotations[img["id"]] = dataset_annotations[img["id"]]

    score_output = compute_score(ds, ground_truth_annotations, predictions, 0)

    image_count = len(sample.keys())
    assert len(predictions) == image_count
    assert len(score_output) == image_count
