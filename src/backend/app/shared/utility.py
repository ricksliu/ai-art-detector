import io
import base64
from PIL import Image
import requests
import shutil
import ast
import numpy as np
from pathlib import Path
from tqdm.auto import tqdm


def create_path(path: str, is_file_path=False):
    """
    Creates the directories to a path location if they do not exist.

    Args:
        path: The path location to create.
        is_file_path: If the path is a path to a file rather than a directory.
    """

    if is_file_path:
        path = '/'.join(path.split('/')[:-1])
    Path(path).mkdir(parents=True, exist_ok=True)


def download_file(url: str, path: str):
    """
    Downloads a file at a URL to a specified path location. Shows a progress bar.

    Args:
        url: The URL of the file to download.
        path: The path location to download the file to.
    """

    with requests.get(url, stream=True) as r:
        create_path(path, is_file_path=True)
        total_length = int(r.headers.get('Content-Length'))  # Get content length in bytes
        with tqdm.wrapattr(r.raw, 'read', total=total_length, desc='') as raw:  # Implement progress bar via tqdm
            with open(path, 'wb') as f:
                shutil.copyfileobj(raw, f)


def base64_to_pil_image(image_base64: str) -> Image.Image:
    """
    Converts a base64 string to a PIL `Image`.

    Args:
        image_base64: The base64 string to convert.

    Returns:
        The converted PIL `Image`.
    """

    image_base64 = image_base64.split('base64,', 1)[1]
    return Image.open(io.BytesIO(base64.b64decode(image_base64)))


def pil_image_to_bytes(image: Image.Image, type: str) -> bytes:
    """
    Converts a PIL `Image` to bytes.

    Args:
        image: The PIL `Image` to convert.
        type: The type of the image.

    Returns:
       The converted bytes.
    """

    image_bytes = io.BytesIO()
    image.save(image_bytes, type)
    return image_bytes.getvalue()


def resize_pil_image(image: Image.Image, min_len: int) -> Image.Image:
    """
    Proportionally resizes a PIL `Image` to a minimum side length.

    Args:
        image: The PIL `Image` to resize.
        min_len: The minimum width and height to resize to.

    Returns:
       The resized PIL `Image`.
    """

    width, height = image.size
    ratio = max(min_len / width, min_len / height)
    return image.resize((round(width * ratio), round(height * ratio)))


def center_crop_np_image(image: np.ndarray, min_len: int) -> np.ndarray:
    """
    Centre crops a numpy image array to a minimum side length.

    Args:
        image: The numpy image array to crop.
        min_len: The minimum width and height to crop to.

    Returns:
       The cropped numpy image array.
    """

    extra_w = (image.shape[0] - min_len) // 2
    extra_h = (image.shape[1] - min_len) // 2
    return image[extra_w:min_len + extra_w, extra_h:min_len + extra_h, :]


def split_np_arr(arr: np.ndarray, proportion: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Splits a numpy array into two.

    Args:
        arr: The numpy array to split.
        proportion: The proportion of the array to split into the first array.

    Returns:
       The two split numpy arrays.
    """

    n = round(arr.shape[0] * proportion)
    return arr.iloc[:n, ...], arr.iloc[n:, ...]


def csv_arr_str_to_np_arr(arr_str: str) -> np.ndarray:
    """
    Converts a CSV array string to a numpy array.

    Args:
        arr_str: The CSV array string to convert.

    Returns:
       The converted numpy array.
    """

    arr_str = ','.join(arr_str.replace('[ ', '[').split())
    return np.array(ast.literal_eval(arr_str))
