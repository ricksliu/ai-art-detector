# Script to download and combine datasets

import os
import pandas as pd
from datasets import load_dataset

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
from django.conf import settings
from shared import utility

def download_laion_dataset():
    if not os.path.isfile(settings.LAION_METADATA_PATH):
        print('Downloading LAION metadata')
        utility.download_file(settings.LAION_METADATA_URL, settings.LAION_METADATA_PATH)

    if len([f for f in os.listdir(settings.LAION_DOWNLOAD_DIR) if f.endswith('.parquet') and not settings.LAION_METADATA_PATH.endswith(f)]) == 0:
        print('Downloading LAION images')
        df = pd.read_parquet(settings.LAION_METADATA_PATH)
        df = df.sample(n=settings.NUM_LAION_SAMPLES, random_state=1)
        df.to_parquet(settings.LAION_TEMP_PATH)
        os.system(settings.LAION_DOWNLOAD_CMD)
        os.remove(settings.LAION_TEMP_PATH)


def map_image_to_bytes(row):
    row['image'] = utility.pil_image_to_bytes(row['image'], 'JPEG')
    return row


def download_diffusiondb_dataset():
    print('Downloading DiffusionDB dataset')
    ds = load_dataset('poloclub/diffusiondb', settings.DIFFUSIONDB_SUBSET, split='train')

    print('Resizing DiffusionDB images')
    ds = ds.map(map_image_to_bytes)
    df = ds.to_pandas()
    df.to_parquet(settings.DIFFUSIONDB_DOWNLOAD_PATH)


def preprocess_laion_dataset():
    print('Preprocessing LAION dataset')
    dfs = [pd.read_parquet(settings.LAION_DOWNLOAD_DIR + f) for f in os.listdir(settings.LAION_DOWNLOAD_DIR) if f.endswith('.parquet') and not settings.LAION_METADATA_PATH.endswith(f)]
    df = pd.concat(dfs).reset_index(drop=True)
    df = df[['jpg']]
    df.rename(columns={'jpg': 'image'}, inplace=True)
    df['is_ai_generated'] = False
    return df


def preprocess_diffusiondb_dataset():
    print('Preprocessing DiffusionDB dataset')
    df = pd.read_parquet(settings.DIFFUSIONDB_DOWNLOAD_PATH)
    df = df[['image']]
    df['is_ai_generated'] = True
    return df


def main():
    print('Downloading datasets')
    download_laion_dataset()
    download_diffusiondb_dataset()

    print('\nPreprocessing datasets')
    dfs = []
    dfs.append(preprocess_laion_dataset())
    dfs.append(preprocess_diffusiondb_dataset())

    print('\nCombining datasets')
    df = pd.concat(dfs).reset_index(drop=True)

    print('\nSaving dataset')
    df.to_parquet(settings.DATASET_PATH)


if __name__ == "__main__":
    main()
