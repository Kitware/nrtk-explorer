from typing import TypeVar, Generic, Tuple

import abc

from PIL import ImageFilter, ImageOps
from PIL.Image import Image

T = TypeVar("T")
S = TypeVar("S")
P = TypeVar("P")


class Transform(abc.ABC, Generic[T, S, P]):
    @abc.abstractmethod
    def execute(self, input: T, *args: P) -> S:
        pass


class ImageTransform(Transform[Image, Image, P]):
    pass


class IdentityTransform(ImageTransform[Tuple[()]]):
    def execute(self, input: Image) -> Image:
        return input.copy()


class GaussianBlurTransform(ImageTransform[Tuple[float]]):
    def execute(self, input: Image, radius: float) -> Image:
        return input.filter(ImageFilter.GaussianBlur(radius))


class InvertTransform(ImageTransform[Tuple[()]]):
    def execute(self, input: Image) -> Image:
        return ImageOps.invert(input)


class DownSampleTransform(ImageTransform[Tuple[int]]):
    def execute(self, input: Image, cx: int) -> Image:
        return input.resize((input.size[0] // cx, input.size[1] // cx))
