import io
import base64
from PIL import Image
import requests
import shutil
import ast
import numpy as np
from pathlib import Path


def create_path(path, is_file_path=False):
    if is_file_path:
        path = '/'.join(path.split('/')[:-1])
    Path(path).mkdir(parents=True, exist_ok=True)


def download_file(url, path):
    with requests.get(url, stream=True) as r:
        create_path(path, is_file_path=True)
        with open(path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def base64_to_pil_image(image_base64):
    image_base64 = image_base64.split('base64,', 1)[1]
    return Image.open(io.BytesIO(base64.b64decode(image_base64)))


def pil_image_to_bytes(image, type):
    image_bytes = io.BytesIO()
    image.save(image_bytes, type)
    return image_bytes.getvalue()


def resize_pil_image(image, min_len):
    width, height = image.size
    ratio = max(min_len / width, min_len / height)
    return image.resize((round(width * ratio), round(height * ratio)))


def center_crop_np_image(image, min_len):
    extra_w = (image.shape[0] - min_len) // 2
    extra_h = (image.shape[1] - min_len) // 2
    return image[extra_w:min_len + extra_w, extra_h:min_len + extra_h, :]


def split_np_arr(arr, percentage):
    n = round(arr.shape[0] * percentage)
    return arr.iloc[:n, ...], arr.iloc[n:, ...]


def csv_arr_str_to_np_arr(arr_str):
    arr_str = ','.join(arr_str.replace('[ ', '[').split())
    return np.array(ast.literal_eval(arr_str))
