import base64
import io
from functools import lru_cache
from PIL import Image
from trame.decorators import TrameApp, change, controller
from nrtk_explorer.app.images.image_ids import (
    dataset_id_to_image_id,
    dataset_id_to_transformed_image_id,
)
from nrtk_explorer.app.images.annotations import DeleteCallbackRef
from nrtk_explorer.app.trame_utils import delete_state
from nrtk_explorer.library.transforms import ImageTransform


IMAGE_CACHE_SIZE = 200


def convert_to_base64(img: Image.Image) -> str:
    """Convert image to base64 string"""
    buf = io.BytesIO()
    img.save(buf, format="png")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


@TrameApp()
class Images:
    def __init__(self, server):
        self.server = server

    @lru_cache(maxsize=IMAGE_CACHE_SIZE)
    def _get_cached_image(self, dataset_id: str):
        image_path = self.server.controller.get_image_fpath(int(dataset_id))
        image = Image.open(image_path)
        image_id = dataset_id_to_image_id(dataset_id)
        self.server.state[image_id] = convert_to_base64(image)
        return DeleteCallbackRef(lambda: delete_state(self.server.state, image_id), image)

    def get_image(self, dataset_id: str):
        return self._get_cached_image(dataset_id).value

    @lru_cache(maxsize=IMAGE_CACHE_SIZE)
    def _get_cached_transformed_image(self, transform: ImageTransform, dataset_id: str):
        original = self.get_image(dataset_id)
        transformed = transform.execute(original)
        if original.size != transformed.size:
            # Resize so pixel-wise annotation similarity score works
            transformed = transformed.resize(original.size)

        image_id = dataset_id_to_transformed_image_id(dataset_id)
        self.server.state[image_id] = convert_to_base64(transformed)
        return DeleteCallbackRef(lambda: delete_state(self.server.state, image_id), transformed)

    def get_transformed_image(self, transform: ImageTransform, dataset_id: str):
        return self._get_cached_transformed_image(transform, dataset_id).value

    @change("current_dataset")
    def clear_all(self, **kwargs):
        self._get_cached_image.cache_clear()
        self.clear_transformed()

    @controller.add("apply_transform")
    def clear_transformed(self, **kwargs):
        self._get_cached_transformed_image.cache_clear()
