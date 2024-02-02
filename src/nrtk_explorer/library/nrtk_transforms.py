from typing import Any, Optional, Dict

from PIL.Image import Image

from nrtk_explorer.library.transforms import ImageTransform, ParameterDescription

from nrtk.impls.perturb_image.generic.cv2.blur import GaussianBlurPerturber


class NrtkGaussianBlurTransform(ImageTransform):
    def __init__(self, perturber: Optional[GaussianBlurPerturber] = None):
        if perturber is None:
            perturber = GaussianBlurPerturber()

        self._perturber: GaussianBlurPerturber = perturber

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "ksize": self._perturber.ksize,
        }

    def set_parameters(self, params: Dict[str, Any]):
        self._perturber.ksize = params.get("ksize", 1)

    def get_parameters_description(self) -> Dict[str, ParameterDescription]:
        ksize_description: ParameterDescription = {
            "type": "integer",
            "label": "Kernel Size",
            "default": 1,
            "description": None,
            "options": None,
        }

        return {
            "ksize": ksize_description,
        }

    def execute(self, input: Image) -> Image:
        return self._perturber.perturb(input)


class NrtkPybsmTransform(ImageTransform):
    def __init__(self, perturber=None):
        # self._perturber = perturber
        pass

    def get_parameters(self) -> dict[str, Any]:
        return {
            # "D": self._perturber.sensor.D,
            # "f": self._perturber.sensor.f,
            "D": 28.0,
            "f": 50.0,
        }

    def set_parameters(self, params: Dict[str, Any]):
        # self._perturber.sensor.D = params["D"]
        # self._perturber.sensor.f = params["f"]
        # self._perturber.metrics = pybsm.niirs(self.sensor, self.scenario)
        pass

    def get_parameters_description(self) -> Dict[str, ParameterDescription]:
        aperture_description: ParameterDescription = {
            "type": "float",
            "label": "Effective Aperture (m)",
            "default": None,
            "description": None,
            "options": None,
        }

        focal_description: ParameterDescription = {
            "type": "float",
            "label": "Focal Length (m)",
            "default": None,
            "description": None,
            "options": None,
        }

        return {
            "D": aperture_description,
            "f": focal_description,
        }

    def execute(self, input: Image, input_parameters=None) -> Image:
        if input_parameters is None:
            input_parameters = {"img_gsd": 1}

        # return self._perturber.perturb(input, input_parameters)
        return input
