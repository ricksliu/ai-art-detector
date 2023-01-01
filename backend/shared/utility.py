import io
import base64
from PIL import Image


def base64_to_image(image_base64):
    image_base64 = image_base64.split('base64,', 1)[1]
    return Image.open(io.BytesIO(base64.b64decode(image_base64)))
