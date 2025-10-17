from aiohttp import web
import io
from PIL import Image
from trame.decorators import TrameApp, controller
from functools import partial
from nrtk_explorer.app.trame_utils import change_checker, delete_state
from nrtk_explorer.app.images.images import Images
from nrtk_explorer.app.images.image_ids import (
    dataset_id_to_image_id,
    dataset_id_to_transformed_image_id,
)


ORIGINAL_IMAGE_ENDPOINT = "original-image"
TRANSFORM_IMAGE_ENDPOINT = "transform-image"


COMPATIBLE_FORMATS = {"JPG", "JPEG", "PNG", "GIF", "WEBP"}


def is_browser_compatible_image(format):
    # Check if the image format is compatible with web browsers
    if not format:
        return False
    return format.upper() in COMPATIBLE_FORMATS


def ensure_browser_compatible_format(image: Image.Image):
    if is_browser_compatible_image(image.format):
        return image.format
    return "JPEG"


def make_response(image: Image.Image):
    format = ensure_browser_compatible_format(image)
    bytes_io = io.BytesIO()
    image.save(bytes_io, format=format)
    bytes_io.seek(0)
    return web.Response(body=bytes_io.read(), content_type=f"image/{format.lower()}")


async def original_image_endpoint(images: Images, state_id_to_dataset_id, request: web.Request):
    dataset_id = state_id_to_dataset_id[request.match_info["id"]]
    image = images.get_image(dataset_id)
    return make_response(image)


async def transform_image_endpoint(images: Images, state_id_to_dataset_id, request: web.Request):
    dataset_id = state_id_to_dataset_id[request.match_info["id"]]
    image = images.get_transformed_image(dataset_id)
    return make_response(image)


@TrameApp()
class ImageServer:
    def __init__(self, server, images: Images):
        self.server = server
        self.images = images
        self._id_counter = 0
        self._state_id_to_dataset_id = {}
        self._transform_keys = set()

        self._endpoint_handler = partial(
            original_image_endpoint, images, self._state_id_to_dataset_id
        )
        self._transform_endpoint_handler = partial(
            transform_image_endpoint,
            images,
            self._state_id_to_dataset_id,
        )

        self.url_prefix = (
            f"/api/{self.server.context.session}" if self.server.context.session else ""
        )

        change_checker(self.server.state, "dataset_ids")(self.on_dataset_ids_change)

    @controller.add("on_server_bind")
    def app_available(self, wslink_server, **kwargs):
        """Add our custom REST endpoints to the trame server."""
        image_routes = [
            web.get(f"/{ORIGINAL_IMAGE_ENDPOINT}/{{id}}", self._endpoint_handler),
            web.get(f"/{TRANSFORM_IMAGE_ENDPOINT}/{{id}}", self._transform_endpoint_handler),
        ]
        wslink_server.app.add_routes(image_routes)

    def on_dataset_ids_change(self, old_ids, new_ids):
        if old_ids is not None:
            to_clean = set(old_ids) - set(new_ids)
            for id in to_clean:
                delete_state(self.server.state, dataset_id_to_image_id(id))
                delete_state(self.server.state, dataset_id_to_transformed_image_id(id))
                keys_to_delete = [k for k, v in self._state_id_to_dataset_id.items() if v == id]
                for key in keys_to_delete:
                    del self._state_id_to_dataset_id[key]
                    if key in self._transform_keys:
                        self._transform_keys.remove(key)

        to_add = set(new_ids) - set(old_ids) if old_ids is not None else new_ids
        for id in to_add:
            # Original
            self._id_counter += 1
            orig_key = str(self._id_counter)
            self._state_id_to_dataset_id[orig_key] = id
            self.server.state[dataset_id_to_image_id(id)] = (
                f"{self.url_prefix}/{ORIGINAL_IMAGE_ENDPOINT}/{orig_key}"
            )

            # Transform
            self._id_counter += 1
            trans_key = str(self._id_counter)
            self._state_id_to_dataset_id[trans_key] = id
            self._transform_keys.add(trans_key)
            self.server.state[dataset_id_to_transformed_image_id(id)] = (
                f"{self.url_prefix}/{TRANSFORM_IMAGE_ENDPOINT}/{trans_key}"
            )

    @controller.add("apply_transform")
    def refresh_transform_images(self, **kwargs):
        for id in self.server.state.dataset_ids:
            self._id_counter += 1
            trans_key = str(self._id_counter)
            self._state_id_to_dataset_id[trans_key] = id
            self._transform_keys.add(trans_key)
            self.server.state[dataset_id_to_transformed_image_id(id)] = (
                f"{self.url_prefix}/{TRANSFORM_IMAGE_ENDPOINT}/{trans_key}"
            )
