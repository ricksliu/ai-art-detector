# Script to predict with model

import os
import numpy as np
from tensorflow import keras

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
from django.conf import settings
from shared import utility


model = keras.models.load_model(settings.MODELS_DIR + settings.MODEL_VER, compile = True)


def predict_is_ai_generated(image):
    image = utility.resize_pil_image(image.convert('RGB'), settings.IMAGE_LEN)
    image = np.divide(np.asarray(image), 255)
    predictions = model.predict(np.asarray([image]))
    return float(predictions[0][0])
