import base64
import io
from functools import lru_cache
from PIL import Image
from trame.app import get_server
from nrtk_explorer.app.images.image_ids import (
    dataset_id_to_transformed_image_id,
)
from nrtk_explorer.app.trame_utils import delete_state
from nrtk_explorer.library.transforms import ImageTransform


IMAGE_CACHE_SIZE = 50


def convert_to_base64(img: Image.Image) -> str:
    """Convert image to base64 string"""
    buf = io.BytesIO()
    img.save(buf, format="png")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


server = get_server()
state, context, ctrl = server.state, server.context, server.controller


class RefCountedState:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __del__(self):
        delete_state(state, self.key)


@lru_cache(maxsize=IMAGE_CACHE_SIZE)
def get_image(dataset_id: str):
    image_path = server.controller.get_image_fpath(int(dataset_id))
    image = Image.open(image_path)
    return image


@lru_cache(maxsize=IMAGE_CACHE_SIZE)
def get_cached_transformed_image(transform: ImageTransform, dataset_id: str):
    key = dataset_id_to_transformed_image_id(dataset_id)

    original = get_image(dataset_id)
    transformed = transform.execute(original)
    if original.size != transformed.size:
        # Resize so pixel-wise annotation similarity score works
        transformed = transformed.resize(original.size)

    state[key] = convert_to_base64(transformed)
    return RefCountedState(key, transformed)


def get_transformed_image(transform: ImageTransform, dataset_id: str):
    return get_cached_transformed_image(transform, dataset_id).value


@state.change("current_dataset")
def clear_all(**kwargs):
    get_image.cache_clear()
    get_cached_transformed_image.cache_clear()


def clear_transformed(**kwargs):
    get_cached_transformed_image.cache_clear()


ctrl.apply_transform.add(clear_transformed)
