from typing import TypeVar, Generic, Dict, TypedDict, Literal, Union, Any, Sequence, Optional

import abc

from PIL import ImageFilter, ImageOps
from PIL.Image import Image

T = TypeVar("T")
S = TypeVar("S")

ParameterType = Literal["string", "integer", "float", "boolean"]
ParameterValue = Union[str, int, float]
ParameterOptions = Sequence[ParameterValue]


# If we target python>=3.11 we should use NotRequired instead of Optional
class ParameterDescription(TypedDict):
    type: ParameterType
    label: str
    description: Optional[str]
    default: Optional[ParameterValue]
    options: Optional[ParameterOptions]


class Transform(abc.ABC, Generic[T, S]):
    @abc.abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @abc.abstractmethod
    def set_parameters(self, params: Dict[str, Any]):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_parameters_description(self) -> Dict[str, ParameterDescription]:
        raise NotImplementedError()

    @abc.abstractmethod
    def execute(self, input: T, *input_args: Any) -> S:
        raise NotImplementedError()


class ImageTransform(Transform[Image, Image]):
    pass


class IdentityTransform(ImageTransform):
    def get_parameters(self) -> Dict[str, Any]:
        return {}

    def set_parameters(self, params: Dict[str, Any]):
        pass

    def get_parameters_description(self) -> Dict[str, ParameterDescription]:
        return {}

    def execute(self, input: Image, *input_args: Any) -> Image:
        return input.copy()


class GaussianBlurTransform(ImageTransform):
    default_radius = 1

    def __init__(self):
        self._radius = GaussianBlurTransform.default_radius

    def get_parameters(self) -> Dict[str, Any]:
        return {"radius": self._radius}

    def set_parameters(self, params: Dict[str, Any]):
        self._radius = params.get("radius", GaussianBlurTransform.default_radius)

    def get_parameters_description(self) -> Dict[str, ParameterDescription]:
        radius_description: ParameterDescription = {
            "type": "integer",
            "default": GaussianBlurTransform.default_radius,
            "label": "Radius",
            "description": None,
            "options": None,
        }

        return {
            "radius": radius_description,
        }

    def execute(self, input: Image, *input_args: Any) -> Image:
        return input.filter(ImageFilter.GaussianBlur(self._radius))


class InvertTransform(ImageTransform):
    def get_parameters(self) -> dict[str, Any]:
        return {}

    def set_parameters(self, params: Dict[str, Any]):
        pass

    def get_parameters_description(self) -> Dict[str, ParameterDescription]:
        return {}

    def execute(self, input: Image, *input_args: Any) -> Image:
        return ImageOps.invert(input)


class DownSampleTransform(ImageTransform):
    def get_parameters(self) -> dict[str, Any]:
        return {}

    def set_parameters(self, params: Dict[str, Any]):
        pass

    def get_parameters_description(self) -> Dict[str, ParameterDescription]:
        return {}

    def execute(self, input: Image, *input_args: Any) -> Image:
        cx = 2
        return input.resize((input.size[0] // cx, input.size[1] // cx))


class TestTransform(ImageTransform):
    default_string = "abc"
    default_int = 7
    default_float = 3.14
    default_boolean = True
    default_select = "two"

    def __init__(self):
        self._string_value = TestTransform.default_string
        self._int_value = TestTransform.default_int
        self._float_value = TestTransform.default_float
        self._boolean_value = TestTransform.default_boolean
        self._select_value = TestTransform.default_select

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "string_param": self._string_value,
            "int_param": self._int_value,
            "float_param": self._float_value,
            "boolean_param": self._boolean_value,
            "select_param": self._select_value,
        }

    def set_parameters(self, params: Dict[str, Any]):
        self._string_value = params.get("string_param", TestTransform.default_string)
        self._int_value = params.get("int_param", TestTransform.default_int)
        self._float_value = params.get("float_param", TestTransform.default_float)
        self._boolean_value = params.get("boolean_param", TestTransform.default_boolean)
        self._select_value = params.get("select_param", TestTransform.default_select)

    def get_parameters_description(self) -> Dict[str, ParameterDescription]:
        string_description: ParameterDescription = {
            "type": "string",
            "default": TestTransform.default_string,
            "label": "A String",
            "description": None,
            "options": None,
        }

        int_description: ParameterDescription = {
            "type": "integer",
            "default": TestTransform.default_int,
            "label": "An Integer",
            "description": None,
            "options": None,
        }

        float_description: ParameterDescription = {
            "type": "float",
            "default": TestTransform.default_float,
            "label": "A Float",
            "description": None,
            "options": None,
        }

        boolean_description: ParameterDescription = {
            "type": "boolean",
            "default": TestTransform.default_boolean,
            "label": "A Boolean",
            "description": None,
            "options": None,
        }

        select_description: ParameterDescription = {
            "type": "string",
            "default": TestTransform.default_select,
            "label": "A Select",
            "description": None,
            "options": ["one", "two", "three", "four"],
        }

        return {
            "string_param": string_description,
            "int_param": int_description,
            "float_param": float_description,
            "boolean_param": boolean_description,
            "select_param": select_description,
        }

    def execute(self, input: Image, *input_args: Any) -> Image:
        return input.copy()
