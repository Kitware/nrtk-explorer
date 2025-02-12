import gc
import logging
import torch
import transformers
from typing import Optional, Sequence, Dict, NamedTuple
from PIL.Image import Image
import math


ImageIdToAnnotations = dict[str, Sequence[dict]]


class ImageWithId(NamedTuple):
    id: str
    image: Image


STARTING_BATCH_SIZE = 32


class Predictor:

    def __init__(
        self,
        model_name: str = "facebook/detr-resnet-50",
        task: Optional[str] = None,
        force_cpu: bool = False,
    ):
        self.task = task
        self.device = "cuda" if torch.cuda.is_available() and not force_cpu else "cpu"
        self.pipeline = model_name
        self.reset()

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
        self._pipeline = transformers.pipeline(
            model=model_name, device=self.device, task=self.task, use_fast=True
        )
        # Do not display warnings
        transformers.utils.logging.set_verbosity_error()

    def reset(self):
        self.batch_size = STARTING_BATCH_SIZE

    def eval(
        self,
        images: Dict[str, Image],
        batch_size: int = 0,  # 0 means use last successful batch size
    ) -> ImageIdToAnnotations:
        """Compute object recognition. Returns Annotations grouped by input image paths."""
        if len(images) == 0:
            return {}  # optimization

        images_with_ids = [ImageWithId(id, img) for id, img in images.items()]

        # Some models require all the images in a batch to be the same size,
        # otherwise crash or UB.
        batches: dict = {}
        for image in images_with_ids:
            size = image.image.size
            exif_data = image.image.getexif()
            orientation = exif_data.get(274, None)
            # Swap dimensions if the orientation implies a 90° rotation
            if orientation in [5, 6, 7, 8]:
                size = (size[1], size[0])
            batches.setdefault(size, [])
            batches[size].append(image)

        if batch_size != 0:
            self.batch_size = self.batch_size
        images_in_batch_count = -1  # for adjusting batch size.
        while self.batch_size > 0:
            try:
                predictions_in_baches = []
                for imagesInBatch in batches.values():
                    image_ids = [image.id for image in imagesInBatch]
                    image_data = [image.image for image in imagesInBatch]
                    images_in_batch_count = len(image_data)
                    pipeline_output = self.pipeline(image_data, batch_size=self.batch_size)
                    predictions_in_baches.append(zip(image_ids, pipeline_output))

                predictions_by_image_id = {
                    image_id: predictions
                    for batch in predictions_in_baches
                    for image_id, predictions in batch
                }
                return predictions_by_image_id

            except RuntimeError as e:
                if "out of memory" in str(e) and self.batch_size > 1:
                    previous_batch_size = self.batch_size
                    image_count_that_failed = min(images_in_batch_count, self.batch_size)
                    # next lower power of 2
                    self.batch_size = 2 ** int(math.log2(image_count_that_failed - 1))
                    print(
                        f"Changing pipeline batch_size from {previous_batch_size} to {self.batch_size} because caught out of memory exception:\n{e}"
                    )
                else:
                    raise

            finally:
                # Pytorch needs to freed its allocations outside of the exception context
                gc.collect()
                torch.cuda.empty_cache()

        # We should never reach here
        return {}
