from PIL.Image import Image
from PIL import Image as ImageModule

import base64
import copy
import io

# Resolution for images to be used in model
IMAGE_MODEL_RESOLUTION = (224, 224)
THUMBNAIL_RESOLUTION = (250, 250)


def convert_to_base64(img: Image) -> str:
    """Convert image to base64 string"""
    buf = io.BytesIO()
    img.save(buf, format="png")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


class ImagesManager:
    """Class to manage images and thumbnails"""

    def __init__(self):
        self.images = {}
        self.thumbnails = {}
        self.images_for_model = {}

    def prepare_for_model(self, img):
        """Prepare image for model input"""
        img = img.resize(IMAGE_MODEL_RESOLUTION)
        return img.convert("RGB")

    def load_image(self, path):
        """Load image from path and store it in cache if not already loaded"""
        if path not in self.images:
            self.images[path] = ImageModule.open(path)

        return self.images[path]

    def load_image_for_model(self, path):
        """Load image for model from path and store it in cache if not already loaded"""
        if path not in self.images_for_model:
            img = copy.copy(self.load_image(path))
            self.images_for_model[path] = self.prepare_for_model(img)

        return self.images_for_model[path]

    def load_thumbnail(self, path):
        """Load thumbnail from path and store it in cache if not already loaded"""
        if path not in self.thumbnails:
            img = copy.copy(self.load_image(path))
            img.thumbnail(THUMBNAIL_RESOLUTION)
            self.thumbnails[path] = img

        return self.thumbnails[path]
