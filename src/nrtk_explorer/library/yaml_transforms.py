import os
import numpy as np
import contextlib

from PIL import Image as ImageModule
from pathlib import Path
from yaml import load, Loader

TRANSFORM_FILE = Path(__file__).with_name("nrtk_transforms.yaml").resolve()

if "NRTK_TRANSFORM_DEFINITION" in os.environ:
    tf = Path(os.environ["NRTK_TRANSFORM_DEFINITION"]).resolve()
    if tf.exists():
        print(f"Using transform definition: {tf}")
        TRANSFORM_FILE = tf
    else:
        print(f"Invalid transform file path: {tf}")


TRANSFORM_DEFINITIONS = load(TRANSFORM_FILE.read_text(), Loader=Loader)

__all__ = [
    "generate_transforms",
]

# -----------------------------------------------------------------------------
# Public
# -----------------------------------------------------------------------------


def generate_transforms():
    transforms = {}
    for k, v in TRANSFORM_DEFINITIONS.items():
        with contextlib.suppress(ModuleNotFoundError):
            transforms[k] = GenericPerturber(v)

    return transforms


# -----------------------------------------------------------------------------
# Internal
# -----------------------------------------------------------------------------


def get(name):
    component_path = name.split(".")
    import_path = ".".join(component_path[:-1])
    obj_name = component_path[-1]
    module = __import__(import_path, fromlist=[obj_name])
    return getattr(module, obj_name)


# -----------------------------------------------------------------------------


def get_value(obj, attr_path):
    v = obj
    for attr in attr_path:
        v = getattr(v, attr)
    return v


# -----------------------------------------------------------------------------


def set_value(obj, attr_path, value):
    attr_path = list(attr_path)
    last_key = attr_path.pop()
    container = obj
    for attr in attr_path:
        container = getattr(container, attr)
    setattr(container, last_key, value)


# -----------------------------------------------------------------------------


def create_perturber_instance(klass, kwargs):
    klass = get(klass)

    if isinstance(kwargs, str):
        kwargs = get(kwargs)

    if callable(kwargs):
        kwargs = kwargs()

    if not isinstance(kwargs, dict):
        raise ValueError(f"kwarg must lead to a dict but got {type(kwargs)}")

    return klass(**kwargs)


# -----------------------------------------------------------------------------


class GenericPerturber:
    def __init__(self, config):
        self.description = config.get("description")
        self.exec_args = config.get("exec_default_args", [])

        # klass
        klass = config.get("perturber")
        kwargs = config.get("perturber_kwargs", {})
        self._perturber = create_perturber_instance(klass, kwargs)

    def get_parameters(self):
        params = {}
        for k, v in self.description.items():
            attr_path = v.get("_path", [k])
            params[k] = get_value(self._perturber, attr_path)
        return params

    def set_parameters(self, params):
        for k, v in params.items():
            attr_path = self.description.get(k).get("_path", [k])
            set_value(self._perturber, attr_path, v)

    def get_parameters_description(self):
        return self.description

    def execute(self, input, *input_args):
        if len(input_args) == 0:
            input_args = self.exec_args

        input_array = np.asarray(input)
        output_array = self._perturber.perturb(input_array, *input_args)

        return ImageModule.fromarray(output_array)