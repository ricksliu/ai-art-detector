# Script to preprocess dataset
# python -m data.preprocess

import os
import sys
import numpy as np
import pandas as pd
from io import BytesIO
from PIL import Image

from shared.utility import resize_pil_image, center_crop_np_image, split_np_arr

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
from django.conf import settings  # noqa: E402


def main():
    multiple_crop = '-multiplecrop' in sys.argv
    mirror = '-mirror' in sys.argv

    print('Reading dataset:')
    df = pd.read_parquet(settings.DATASET_PATH)
    print(f'- total: {len(df)}')

    print('Removing invalid images:')
    df.dropna(inplace=True)  # Remove rows that contain null values
    df.reset_index(drop=True, inplace=True)
    print(f'- total: {len(df)}')

    print('Resizing images')
    df['image'] = df['image'].apply(lambda i: resize_pil_image(Image.open(BytesIO(i)).convert('RGB'), settings.IMAGE_LEN))

    print('Normalizing images')
    df['image'] = df['image'].apply(lambda i: np.asarray(i))
    df['image'] = df['image'].apply(lambda i: i if i.ndim == 3 else None)
    df['image'] = df['image'].apply(lambda i: np.divide(i, 255))

    print('Cropping images:')
    df['image'] = df['image'].apply(lambda i: center_crop_np_image(i, settings.IMAGE_LEN))
    if multiple_crop:
        pass
    print(f'- total: {len(df)}')

    if mirror:
        print('Mirroring images:')
        df_mirrored = df.copy()
        df_mirrored['image'] = df_mirrored['image'].apply(lambda i: np.flip(i, axis=1))
        df = pd.concat([df, df_mirrored]).reset_index(drop=True)
        print(f'- total: {len(df)}')

    print('Splitting into train and test datasets:')
    df = df.sample(frac=1).reset_index(drop=True)
    train, test = split_np_arr(df, 0.8)
    print(f'- train: {len(train)}')
    print(f'- test: {len(test)}')

    print('Saving datasets:')
    train.to_pickle(settings.TRAIN_SET_PATH)
    test.to_pickle(settings.TEST_SET_PATH)
    print(f'- total: {len(train)} + {len(test)} = {len(df)}')


if __name__ == "__main__":
    main()
