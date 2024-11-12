from nrtk_explorer.library.dataset import get_dataset, JsonDataset
import nrtk_explorer.test_data

from pathlib import Path

import pytest


@pytest.fixture
def dataset_path():
    dir_name = Path(nrtk_explorer.test_data.__file__).parent
    return f"{dir_name}/coco-od-2017/test_val2017.json"


def test_get_dataset(dataset_path):
    ds1 = get_dataset(dataset_path)
    assert ds1 is not None

    ds1 = get_dataset(dataset_path)
    ds2 = get_dataset(dataset_path)
    assert ds1 is ds2


def test_get_dataset_empty():
    with pytest.raises(ValueError):
        get_dataset("nonexisting")


def test_DefaultDataset(dataset_path):
    ds = JsonDataset(dataset_path)
    assert len(ds.imgs) > 0
    assert len(ds.cats) > 0
    assert len(ds.anns) > 0
    assert ds.get_image(next(iter(ds.imgs.keys()))) is not None
