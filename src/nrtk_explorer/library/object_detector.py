import logging
import operator
import torch
import transformers

from functools import reduce
from typing import Optional

from nrtk_explorer.library import images_manager

Annotation = dict  # in COCO format
Annotations = list[Annotation]
ImageId = str
AnnotatedImage = tuple[ImageId, Annotations]
AnnotatedImages = list[AnnotatedImage]


class ObjectDetector:
    """Object detection using Hugging Face's transformers library"""

    def __init__(
        self,
        model_name: str = "facebook/detr-resnet-50",
        task: Optional[str] = None,
        manager: Optional[images_manager.ImagesManager] = None,
        force_cpu: bool = False,
    ):
        if manager is None:
            manager = images_manager.ImagesManager()

        self.task = task
        self.manager = manager
        self.device = "cuda" if torch.cuda.is_available() and not force_cpu else "cpu"
        self.pipeline = model_name

    @property
    def device(self) -> str:
        """Get the device to use for feature extraction"""
        return str(self._device)

    @device.setter
    def device(self, dev: str):
        """Set the device to use for feature extraction"""
        logging.info(f"Using {dev} devices for feature extraction")
        self._device = torch.device(dev)

    @property
    def pipeline(self) -> transformers.pipeline:
        """Get the pipeline for object detection using Hugging Face's transformers library"""
        return self._pipeline

    @pipeline.setter
    def pipeline(self, model_name: str):
        """Set the pipeline for object detection using Hugging Face's transformers library"""
        if self.task is None:
            self._pipeline = transformers.pipeline(model=model_name, device=self.device)
        else:
            self._pipeline = transformers.pipeline(
                model=model_name, device=self.device, task=self.task
            )
        # Do not display warnings
        transformers.utils.logging.set_verbosity_error()

    def eval(
        self,
        image_ids: list[str],
        content: Optional[dict] = None,
        batch_size: int = 32,
    ) -> AnnotatedImages:
        """Compute object recognition. Returns Annotations grouped by input image paths."""
        images: dict = {}

        # Some models require all the images in a batch to be the same size,
        # otherwise crash or UB.
        for path in image_ids:
            img = None
            if content and path in content:
                img = content[path]
            else:
                img = self.manager.load_image(path)

            images.setdefault(img.size, [[], []])
            images[img.size][0].append(path)
            images[img.size][1].append(img)

        # Call by each group
        predictions = [
            list(
                zip(
                    group[0],
                    self.pipeline(group[1], batch_size=batch_size),
                )
            )
            for group in images.values()
        ]
        # Flatten the list of predictions
        predictions = reduce(operator.iadd, predictions, [])

        # order output by paths order
        find_prediction = lambda id: next(
            prediction for prediction in predictions if prediction[0] == id
        )
        output = [find_prediction(id) for id in image_ids]
        # mypy wrongly thinks output's type is list[list[tuple[str, dict]]]
        return output  # type: ignore
