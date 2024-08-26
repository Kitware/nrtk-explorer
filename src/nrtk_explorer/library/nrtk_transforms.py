from typing import Any, Dict, Optional, TYPE_CHECKING

import numpy as np
import logging
from PIL import Image as ImageModule
from PIL.Image import Image
from nrtk_explorer.library.transforms import ImageTransform, ParameterDescription

ENABLED_NRTK_TRANSFORMS = True

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

try:
    from pybsm.otf import darkCurrentFromDensity
    from nrtk.impls.perturb_image.generic.cv2.blur import GaussianBlurPerturber
    from nrtk.impls.perturb_image.pybsm.perturber import PybsmPerturber, PybsmSensor, PybsmScenario
except ImportError:
    logger.info("Disabling NRTK transforms due to missing library/failing imports")
    ENABLED_NRTK_TRANSFORMS = False

if TYPE_CHECKING:
    GaussianBlurPerturberType = GaussianBlurPerturber
    PybsmPerturberType = PybsmPerturber
else:
    GaussianBlurPerturberType = None
    PybsmPerturberType = None

GaussianBlurPerturberArg = Optional[GaussianBlurPerturberType]
PybsmPerturberArg = Optional[PybsmPerturberType]


def nrtk_transforms_available():
    return ENABLED_NRTK_TRANSFORMS


class NrtkGaussianBlurTransform(ImageTransform):
    def __init__(self, perturber: GaussianBlurPerturberArg = None):
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

    def execute(self, input: Image, *input_args: Any) -> Image:
        input_array = np.asarray(input)
        output_array = self._perturber.perturb(input_array)

        return ImageModule.fromarray(output_array)


# Taken from the nrtk package tests
# https://github.com/Kitware/nrtk/blob/main/tests/impls/perturb_image/pybsm/test_pybsm_pertuber.py#L21
def createSampleSensorAndScenario():

    name = "L32511x"

    # telescope focal length (m)
    f = 4
    # Telescope diameter (m)
    D = 275e-3

    # detector pitch (m)
    p = 0.008e-3

    # Optical system transmission, red  band first (m)
    optTransWavelengths = np.array([0.58 - 0.08, 0.58 + 0.08]) * 1.0e-6
    # guess at the full system optical transmission (excluding obscuration)
    opticsTransmission = 0.5 * np.ones(optTransWavelengths.shape[0])

    # Relative linear telescope obscuration
    eta = 0.4  # guess

    # detector width is assumed to be equal to the pitch
    wx = p
    wy = p
    # integration time (s) - this is a maximum, the actual integration time will be
    # determined by the well fill percentage
    intTime = 30.0e-3

    # dark current density of 1 nA/cm2 guess, guess mid range for a silicon camera
    darkCurrent = darkCurrentFromDensity(1e-5, wx, wy)

    # rms read noise (rms electrons)
    readNoise = 25.0

    # maximum ADC level (electrons)
    maxN = 96000.0

    # bit depth
    bitdepth = 11.9

    # maximum allowable well fill (see the paper for the logic behind this)
    maxWellFill = 0.6

    # jitter (radians) - The Olson paper says that its "good" so we'll guess 1/4 ifov rms
    sx = 0.25 * p / f
    sy = sx

    # drift (radians/s) - again, we'll guess that it's really good
    dax = 100e-6
    day = dax

    # etector quantum efficiency as a function of wavelength (microns)
    # for a generic high quality back-illuminated silicon array
    # https://www.photometrics.com/resources/learningzone/quantumefficiency.php
    qewavelengths = np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]) * 1.0e-6
    qe = np.array([0.05, 0.6, 0.75, 0.85, 0.85, 0.75, 0.5, 0.2, 0])

    sensor = PybsmSensor(
        name,
        D,
        f,
        p,
        optTransWavelengths,
        opticsTransmission,
        eta,
        wx,
        wy,
        intTime,
        darkCurrent,
        readNoise,
        maxN,
        bitdepth,
        maxWellFill,
        sx,
        sy,
        dax,
        day,
        qewavelengths,
        qe,
    )

    altitude = 9000.0
    # range to target
    groundRange = 60000.0

    scenario_name = "niceday"
    # weather model
    ihaze = 1
    scenario = PybsmScenario(scenario_name, ihaze, altitude, groundRange)
    scenario.aircraftSpeed = 100.0

    return sensor, scenario


class NrtkPybsmTransform(ImageTransform):
    def __init__(self, perturber: PybsmPerturberArg = None):
        if perturber is None:
            sensor, scenario = createSampleSensorAndScenario()
            perturber = PybsmPerturber(sensor=sensor, scenario=scenario)

        self._perturber: PybsmPerturber = perturber

    def get_parameters(self) -> dict[str, Any]:
        return {
            "D": self._perturber.sensor.D,
            "f": self._perturber.sensor.f,
        }

    def set_parameters(self, params: Dict[str, Any]):
        self._perturber.sensor.D = params["D"]
        self._perturber.sensor.f = params["f"]

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

    def execute(self, input: Image, *input_args: Any) -> Image:
        if len(input_args) == 0:
            input_args = ({"img_gsd": 0.15},)

        input_array = np.asarray(input)
        output_array = self._perturber.perturb(input_array, *input_args)

        return ImageModule.fromarray(output_array)
