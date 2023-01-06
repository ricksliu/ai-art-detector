# Script to download and combine datasets
# python -m data.get_dataset

import os
import pandas as pd
import gdown
import ast

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
from django.conf import settings
from shared import utility


def find_metadata_paths(dataset_dir):
    if not os.path.exists(dataset_dir):
        return []
    return [dataset_dir + f for f in os.listdir(dataset_dir) if f.startswith('metadata')]


def find_data_paths(dataset_dir):
    if not os.path.exists(dataset_dir):
        return []
    return [dataset_dir + f for f in os.listdir(dataset_dir) if f.endswith('.parquet') and not f.startswith('metadata')]


# Read a list of paths to data files and return a single dataframe
def read_data(paths, target_num=-1):
    dfs = []
    num = 0
    for path in paths:
        if path.endswith('.parquet'):
            dfs.append(pd.read_parquet(path))

        elif path.endswith('.csv'):
            for chunk in pd.read_csv(path, chunksize=10000):
                dfs.append(chunk)
                if target_num != -1:
                    num += dfs[-1].shape[0]
                    if num >= target_num:
                        break

        if target_num != -1:
            num += dfs[-1].shape[0]
            if num >= target_num:
                break

    return pd.concat(dfs).reset_index(drop=True)


def extract_openprompts_url_metadata(x):
    try:
        return ast.literal_eval(x)
    except:
        return { 'raw_discord_data': { 'image_uri': None } }


# Expose url data in metadata df as a top level column so img2dataset can read it
def format_metadata_df(df, dataset):
    if dataset == 'laion':
        df = df.rename(columns={'URL': 'url'})

    elif dataset == 'openprompts':
        df['raw_data'] = df['raw_data'].apply(lambda x: extract_openprompts_url_metadata(x))
        df['raw_data'] = df['raw_data'].apply(lambda x: x.get('raw_discord_data').get('image_uri'))
        df = df.rename(columns={'raw_data': 'url'})

    return df


def download_dataset(dataset, force_download_metadata=False, force_download_data=False):
    DATASET_DIR = settings.DATA_DIR + 'datasets/{}/'.format(dataset)
    TEMP_METADATA_PATH = DATASET_DIR + 'metadata-temp.parquet'

    metadata_paths = find_metadata_paths(DATASET_DIR)
    if force_download_metadata:
        for path in metadata_paths:
            os.remove(path)

    if len(metadata_paths) == 0:
        print('Downloading {} metadata'.format(dataset))
        for i in range(len(settings.DATASETS[dataset]['metadata'])):
            if settings.DATASETS[dataset]['metadata_src'] == 'url':
                metadata_path = DATASET_DIR + 'metadata-{}.parquet'.format(i)
                utility.download_file(settings.DATASETS[dataset]['metadata'][i], metadata_path)

            elif settings.DATASETS[dataset]['metadata_src'] == 'gdrive':
                metadata_path = DATASET_DIR + 'metadata-{}.{}'.format(i, settings.DATASETS[dataset]['metadata_type'])
                utility.create_path(metadata_path, is_file_path=True)
                gdown.download(settings.DATASETS[dataset]['metadata'][i], metadata_path, quiet=False)
    
    else:
        print('Found existing {} metadata'.format(dataset))

    metadata_paths = find_metadata_paths(DATASET_DIR)
    data_paths = find_data_paths(DATASET_DIR)
    if force_download_data:
        for path in data_paths:
            os.remove(path)

    if len(data_paths) == 0:
        print('Downloading {} images'.format(dataset))
        df = None
        df = read_data(metadata_paths, settings.DATASETS[dataset]['samples'] * 10)
        df = df.sample(n=settings.DATASETS[dataset]['samples'], random_state=1)
        df = format_metadata_df(df, dataset)

        # Temporarily save df so img2dataset can read it
        df.to_parquet(TEMP_METADATA_PATH)
        os.system('img2dataset --url_list {} --input_format "parquet" --output_folder {} --output_format parquet --processes_count 16 --thread_count 64 --image_size {} --encode_format webp --resize_mode="keep_ratio" --skip_reencode=True --url_col "url" --disallowed_header_directives "[]"'.format(TEMP_METADATA_PATH, DATASET_DIR, settings.DOWNLOAD_IMAGE_LEN))
        os.remove(TEMP_METADATA_PATH)

    else:
        print('Found existing {} images'.format(dataset))

    data_paths = find_data_paths(DATASET_DIR)

    print('Preprocessing {} dataset'.format(dataset))
    df = read_data(data_paths)
    df = df[['webp']]
    df.rename(columns={'webp': 'image'}, inplace=True)
    df['is_ai_generated'] = settings.DATASETS[dataset]['is_ai_generated']

    return df


def main():
    print('Downloading datasets')
    dfs = []
    for dataset in settings.DATASETS.keys():
        dfs.append(download_dataset(dataset))

    print('\nCombining datasets')
    df = pd.concat(dfs).reset_index(drop=True)

    print('\nSaving dataset')
    df.to_parquet(settings.DATASET_PATH)


if __name__ == "__main__":
    main()
