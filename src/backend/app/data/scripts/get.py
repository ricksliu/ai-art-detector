# Script to download and combine datasets
# python -m data.get

import os
import sys
import pandas as pd

from shared.utility import download_file

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
from django.conf import settings  # noqa: E402


def get_metadata_paths(dataset_dir: str) -> list[str]:
    """
    Gets the metadata filenames in a given dataset directory.

    Arguments:
        dataset_dir: The directory to search.

    Returns:
        The list of filenames that start with 'metadata'.
    """

    if not os.path.exists(dataset_dir):
        return []
    return [dataset_dir + f for f in os.listdir(dataset_dir) if f.endswith('.parquet') and f.startswith('metadata')]


def get_data_paths(dataset_dir: str) -> list[str]:
    """
    Gets the (non-metadata) data filenames in a given dataset directory.

    Arguments:
        dataset_dir: The directory to search.

    Returns:
        The list of filenames that do not start with 'metadata'.
    """

    if not os.path.exists(dataset_dir):
        return []
    return [dataset_dir + f for f in os.listdir(dataset_dir) if f.endswith('.parquet') and not f.startswith('metadata')]


def read_data(paths: list[str], target_num=-1) -> pd.DataFrame:
    """
    Creates a `DataFrame` from a list of paths to data files.

    Arguments:
        paths: The list of paths to data files.
        target_num: The number of rows in the `DataFrame` to reach before stopping.

    Returns:
        The `DataFrame` with at least `target_num` rows.
    """

    dfs = []
    num = 0
    for path in paths:
        dfs.append(pd.read_parquet(path))
        if target_num != -1:
            num += dfs[-1].shape[0]
            if num >= target_num:
                break

    return pd.concat(dfs).reset_index(drop=True)


def process_metadata(df: pd.DataFrame, dataset: str) -> pd.DataFrame:
    """
    Processes a metadata `DataFrame` in preparation for img2dataset to download it.
    Filters images that do not meet the size requirement.
    Exposes a `url` column for img2dataset to read.

    Arguments:
        df: The metadata `DataFrame` to process.
        dataset: The name of the dataset where the metadata is from. Different datasets structure their metadata differently.

    Returns:
        The processed `DataFrame`.
    """

    if dataset == 'laion':
        df = df[df['WIDTH'] >= settings.DOWNLOAD_IMAGE_LEN]
        df = df[df['HEIGHT'] >= settings.DOWNLOAD_IMAGE_LEN]
        df = df.rename(columns={'URL': 'url'})

    elif dataset == 'stable-diffusion':
        df = df[df['width'] >= settings.DOWNLOAD_IMAGE_LEN]
        df = df[df['height'] >= settings.DOWNLOAD_IMAGE_LEN]
        df = df.rename(columns={'URL': 'url'})

    elif dataset == 'midjourney':
        df = df.rename(columns={'Attachments': 'url'})

    return df


def download_dataset(dataset: str, force_download_metadata=False, force_download_data=False) -> pd.DataFrame:
    """
    Downloads the data for a given `dataset`.

    Arguments:
        dataset: The name of the dataset. Different datasets host their data in different places.
        force_download_metadata: Force re-download the metadata for `dataset`.
        force_download_data Force redownload the data for `dataset`.

    Returns:
        A `DataFrame` containing the data for `dataset`.
    """

    DATASET_DIR = settings.DATA_DIR + 'datasets/{}/'.format(dataset)  # Location to save datasets to
    TEMP_METADATA_PATH = DATASET_DIR + 'metadata-temp.parquet'  # Location to store temporary metadata file

    metadata_paths = get_metadata_paths(DATASET_DIR)

    # Delete existing metadata to force re-download
    if force_download_metadata:
        print('  - Deleting existing metadata')
        for path in metadata_paths:
            os.remove(path)
        metadata_paths = get_metadata_paths(DATASET_DIR)

    # Download metadata
    if len(metadata_paths) == 0:
        print('  - Downloading metadata')
        for i in range(len(settings.DATASETS[dataset]['metadata'])):
            metadata_path = DATASET_DIR + 'metadata-{}.parquet'.format(i)
            download_file(settings.DATASETS[dataset]['metadata'][i], metadata_path)
        metadata_paths = get_metadata_paths(DATASET_DIR)
    else:
        print('  - Found existing metadata')

    data_paths = get_data_paths(DATASET_DIR)

    # Delete existing data to force re-download
    if force_download_data:
        print('  - Deleting existing data')
        for path in data_paths:
            os.remove(path)
        data_paths = get_data_paths(DATASET_DIR)

    # Download data
    if len(data_paths) == 0:
        # Randomly sample a subset of the metadata
        print('  - Sampling metadata')
        df = read_data(metadata_paths, settings.DATASETS[dataset]['samples'] * 5)
        df = process_metadata(df, dataset)
        df = df.sample(n=settings.DATASETS[dataset]['samples'], random_state=1)

        # Download the data associated with the metadata
        print('  - Downloading data')
        for json_file in [DATASET_DIR + f for f in os.listdir(DATASET_DIR) if f.endswith('.json')]:  # Delete previous img2dataset metadata files
            os.remove(json_file)
        df.to_parquet(TEMP_METADATA_PATH)  # Temporarily save df as a file so img2dataset can read it
        os.system('img2dataset --url_list {} --input_format "parquet" --output_folder {} --output_format parquet --processes_count 16 --thread_count 64 --image_size {} --encode_format webp --resize_mode="keep_ratio" --skip_reencode=True --url_col "url" --disallowed_header_directives "[]"'.format(TEMP_METADATA_PATH, DATASET_DIR, settings.DOWNLOAD_IMAGE_LEN))
        os.remove(TEMP_METADATA_PATH)  # Delete temporary df file
        data_paths = get_data_paths(DATASET_DIR)
    else:
        print('  - Found existing data')

    # Preprocess data
    print('  - Labelling data')
    df = read_data(data_paths)
    df = df[['webp']]
    df.rename(columns={'webp': 'image'}, inplace=True)
    df['is_ai_generated'] = settings.DATASETS[dataset]['is_ai_generated']

    return df


def main():
    force_download_metadata = '-fmetadata' in sys.argv
    force_download_data = '-fdata' in sys.argv

    datasets = list(settings.DATASETS.keys())

    print('Downloading datasets:')
    dfs = []
    for dataset in datasets:
        print(f'- {dataset}:')
        dfs.append(download_dataset(dataset, force_download_metadata, force_download_data))

    print('Combining datasets:')
    df = pd.concat(dfs).reset_index(drop=True)
    for i in range(len(datasets)):
        print(f'- {datasets[i]}: {len(dfs[i])}')

    print('Saving dataset:')
    df.to_parquet(settings.DATASET_PATH)
    print(f'- total: {len(df)}')


if __name__ == "__main__":
    main()
