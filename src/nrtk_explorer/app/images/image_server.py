from aiohttp import web
from PIL import Image
import io
from trame.app import get_server
from nrtk_explorer.library.dataset import get_image_path


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
    id = request.match_info["id"]
    image_path = get_image_path(id)

    if image_path in server.context.images_manager.images:
        image = server.context.images_manager.images[image_path]
        send_format = "PNG"
        if is_browser_compatible_image(image.format):
            send_format = image.format.upper()
        return make_response(image, send_format)

    if is_browser_compatible_image(image_path):
        return web.FileResponse(image_path)
    else:
        image = Image.open(image_path)
        return make_response(image, "PNG")


image_routes = [
    web.get(f"/{ORIGINAL_IMAGE_ENDPOINT}/{{id}}", original_image_endpoint),
]


def app_available(wslink_server):
    """Add our custom REST endpoints to the trame server."""
    wslink_server.app.add_routes(image_routes)


# --hot-reload does not work if this is configured as decorator on the function
server.controller.add("on_server_bind")(app_available)
