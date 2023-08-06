import json
import os
import pathlib
import zipfile

import pandas as pd
# self defined functions
from zeroloader.drive import GoogleDrive


def unzip(zip_file):
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(os.path.dirname(zip_file))
        os.remove(zip_file)


def get_producer_month_id(gdrive, producer, month):
    mapping_file_id = os.getenv("GDRIVE_PUBLIC_FILE_MAPPING_ID")
    gdrive.download(mapping_file_id, ".", "public_file_mapping.json")
    mapping = json.load(open(f"public_file_mapping.json", "r"))
    return mapping[producer][month]


def download_data(gdrive, producer, month):
    item_id = get_producer_month_id(gdrive, producer, month)
    dest_dir = f'/tmp/0archive/{producer}/{month}'
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    unzip(gdrive.download(id=item_id, output_dir=dest_dir))
    data_dir = pathlib.Path(dest_dir)

    return data_dir


def load_data(producer, month, service_file='service.json'):
    """
    works with one month only
    """
    gdrive = GoogleDrive(service_file)
    data_dir = download_data(gdrive, producer, month)

    df_all = pd.concat([
        pd.read_json(json_file, lines=True, encoding="utf-8")
        for json_file in data_dir.glob(f"{month}-*.jsonl")
    ], ignore_index=True)

    return df_all