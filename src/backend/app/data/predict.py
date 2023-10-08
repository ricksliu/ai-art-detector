# Script to predict with model

import os
import numpy as np
import torch
from PIL import Image

from shared.utility import resize_pil_image, center_crop_np_image
from data.ml.network import Network

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
from django.conf import settings  # noqa: E402


model = Network()
model.load_state_dict(torch.load(
    settings.MODELS_DIR + settings.MODEL_VER + '/' + settings.MODEL_NAME,
    map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu'),
))
model.eval()


def predict_is_ai_generated(image: Image.Image) -> float:
    """
    Return the model's prediction for a PIL `Image`.

    Arguments:
        image: The PIL `Image` to predict.

    Returns:
        The model's prediction.
    """

    image = resize_pil_image(image.convert('RGB'), settings.IMAGE_LEN)  # Resize image
    image = center_crop_np_image(np.asarray(image), settings.IMAGE_LEN)  # Crop image
    image = np.divide(image, 255)  # Normalize image
    image = np.moveaxis(image, 2, 0)  # Reshape image channel ordering

    x = torch.Tensor(np.asarray([image])).type(torch.FloatTensor)

    # Predict
    with torch.no_grad():
        pred = model(x)
        return float(pred.data[0][1])
