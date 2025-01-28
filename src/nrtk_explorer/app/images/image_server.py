from aiohttp import web
import io
from PIL import Image
from trame.decorators import TrameApp, controller
from functools import partial
from nrtk_explorer.app.trame_utils import change_checker, delete_state

from nrtk_explorer.app.images.image_ids import dataset_id_to_image_id


ORIGINAL_IMAGE_ENDPOINT = "original-image"


def is_browser_compatible_image(file_path):
    # Check if the image format is compatible with web browsers
    compatible_formats = {"jpg", "jpeg", "png", "gif", "webp"}
    return file_path.split(".")[-1].lower() in compatible_formats


def ensure_browser_compatable_foramt(image: Image.Image):
    if is_browser_compatible_image(image.format):
        return image.format
    return "JPEG"


def make_response(image: Image.Image):
    format = ensure_browser_compatable_foramt(image)
    bytes_io = io.BytesIO()
    image.save(bytes_io, format=format)
    bytes_io.seek(0)
    return web.Response(body=bytes_io.read(), content_type=f"image/{format.lower()}")


async def original_image_endpoint(images, state_id_to_dataset_id, request: web.Request):
    dataset_id = state_id_to_dataset_id[request.match_info["id"]]
    image = images.get_image(dataset_id)
    return make_response(image)


@TrameApp()
class ImageServer:
    def __init__(self, server, images):
        self.server = server
        self._state_id_to_dataset_id = {}
        self._endpoint_handler = partial(
            original_image_endpoint, images, self._state_id_to_dataset_id
        )
        self._stateManager = StatefullImages(server, self._state_id_to_dataset_id)

    @controller.add("on_server_bind")
    def app_available(self, wslink_server, **kwargs):
        """Add our custom REST endpoints to the trame server."""
        image_routes = [
            web.get(f"/{ORIGINAL_IMAGE_ENDPOINT}/{{id}}", self._endpoint_handler),
        ]
        wslink_server.app.add_routes(image_routes)


@TrameApp()
class StatefullImages:
    def __init__(self, server, state_id_to_dataset_id):
        self.server = server
        self._state_id_to_dataset_id = state_id_to_dataset_id
        self._id_counter = 0
        change_checker(self.server.state, "dataset_ids")(self.on_dataset_ids_change)

    def on_dataset_ids_change(self, old_ids, new_ids):
        if old_ids is not None:
            to_clean = set(old_ids) - set(new_ids)
            for id in to_clean:
                delete_state(self.server.state, dataset_id_to_image_id(id))
                if id in self._state_id_to_dataset_id.values():
                    key_to_delete = next(
                        k for k, v in self._state_id_to_dataset_id.items() if v == id
                    )
                    del self._state_id_to_dataset_id[key_to_delete]

        to_add = set(new_ids) - set(old_ids) if old_ids is not None else new_ids
        for id in to_add:
            self._id_counter += 1
            self._state_id_to_dataset_id[str(self._id_counter)] = id
            self.server.state[dataset_id_to_image_id(id)] = (
                f"/{ORIGINAL_IMAGE_ENDPOINT}/{self._id_counter}"
            )
