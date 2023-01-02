import io
import base64
from PIL import Image
import requests
import shutil


def download_file(url, path):
    with requests.get(url, stream=True) as r:
        with open(path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def base64_to_image(image_base64):
    image_base64 = image_base64.split('base64,', 1)[1]
    return Image.open(io.BytesIO(base64.b64decode(image_base64)))
