import io
import base64

from PIL.Image import Image


def image_to_base64_str(img: Image, format: str) -> str:
    buf = io.BytesIO()
    img.save(buf, format=format)
    return f"data:image/{format};base64," + base64.b64encode(buf.getvalue()).decode()
