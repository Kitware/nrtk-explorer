from utils import get_image

from nrtk_explorer.library.yaml_transforms import (
    generate_transforms,
)


def test_gaussian_blur():
    transforms = generate_transforms()
    blur = transforms["nrtk_blur_2"]
    blur.set_parameters({"ksize": 3})
    blur.execute(get_image())


def test_pybsm():
    transforms = generate_transforms()
    pybsm = transforms["nrtk_pybsm_2"]
    pybsm.set_parameters({"D": 0.25, "f": 4.0})
    pybsm.execute(get_image())
