# Script to preprocess dataset
# python -m data.preprocess_dataset

import os
import numpy as np
import pandas as pd
from io import BytesIO
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
from django.conf import settings
from shared import utility


def main():
    print('Loading dataset')
    df = pd.read_parquet(settings.DATASET_PATH)

    print('\nRemoving invalid data')
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    print('\nResizing images')
    df['image'] = df['image'].apply(lambda i: utility.resize_pil_image(Image.open(BytesIO(i)).convert('RGB'), settings.IMAGE_LEN))

    print('\nNormalizing image data')
    df['image'] = df['image'].apply(lambda i: np.asarray(i))
    df['image'] = df['image'].apply(lambda i: i if i.ndim == 3 else None)
    df['image'] = df['image'].apply(lambda i: np.divide(i, 255))

    print('\nCropping images')
    df['image'] = df['image'].apply(lambda i: utility.center_crop_np_image(i, settings.IMAGE_LEN))

    print('\nReflecting images')
    df_reflected = df.copy()
    df_reflected['image'] = df_reflected['image'].apply(lambda i: np.flip(i, axis=1))
    df = pd.concat([df, df_reflected]).reset_index(drop=True)

    print('\nSplitting dataset')
    df = df.sample(frac=1).reset_index(drop=True)
    train, test = utility.split_np_arr(df, 0.8)

    print('\nSaving dataset')
    train.to_pickle(settings.TRAIN_SET_PATH)
    test.to_pickle(settings.TEST_SET_PATH)


if __name__ == "__main__":
    main()
