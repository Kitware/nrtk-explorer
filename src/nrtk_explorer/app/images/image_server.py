from aiohttp import web
import io
from trame.app import get_server
from nrtk_explorer.app.images.images import get_image


ORIGINAL_IMAGE_ENDPOINT = "original-image"

server = get_server()


def is_browser_compatible_image(file_path):
    # Check if the image format is compatible with web browsers
    compatible_formats = {"jpg", "jpeg", "png", "gif", "webp"}
    return file_path.split(".")[-1].lower() in compatible_formats


def make_response(image, format):
    bytes_io = io.BytesIO()
    image.save(bytes_io, format=format)
    bytes_io.seek(0)
    return web.Response(body=bytes_io.read(), content_type=f"image/{format.lower()}")


async def original_image_endpoint(request: web.Request):
    dataset_id = request.match_info["id"]
    image = get_image(dataset_id)
    if is_browser_compatible_image(image.format):
        send_format = image.format.upper()
    else:
        send_format = "PNG"
    return make_response(image, send_format)


image_routes = [
    web.get(f"/{ORIGINAL_IMAGE_ENDPOINT}/{{id}}", original_image_endpoint),
]


def app_available(wslink_server):
    """Add our custom REST endpoints to the trame server."""
    wslink_server.app.add_routes(image_routes)


# --hot-reload does not work if this is configured as decorator on the function
server.controller.add("on_server_bind")(app_available)
