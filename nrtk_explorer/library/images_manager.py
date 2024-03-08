from PIL.Image import Image
from PIL import Image as ImageModule

import base64
import io


def image_to_base64_str(img: Image, format: str) -> str:
    buf = io.BytesIO()
    img.save(buf, format=format)
    return f"data:image/{format};base64," + base64.b64encode(buf.getvalue()).decode()


class ImagesManager:
    def __init__(self, server_context=None):
        if server_context:
            server_context["images_cache"] = {}
            self.images = server_context["images_cache"]
        else:
            self.images = {}

    def LoadImage(self, path):
        if path not in self.images:
            img = ImageModule.open(path)
            w, h = img.size
            ratio = w / h

            new_w = min(w, 224)
            new_h = round(new_w / ratio)

            img = img.resize((new_w, new_h))
            img = img.convert("RGB")
            self.images[path] = img

        return self.images[path]

    def ComputeBase64(self, img_id, img):
        return image_to_base64_str(img, "png")
