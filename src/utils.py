import yaml
import pandas as pd
import os
import base64


def load_config(file_path: str = "config.yaml") -> dict:
    """
    load config file into dict python object
    """
    try:
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
    except Exception as e:
        print(f"Fail to load config file because of {e}")
        config = {}
    return config


def load_features_and_meta(config: dict) -> pd.DataFrame:
    try:
        meta_data = pd.read_csv(
            os.path.join(
                config["data"]["data_folder"], config["data"]["etude_1000_filename"]
            ),
            sep=",",
        )
        features = pd.read_csv(
            os.path.join(
                config["data"]["data_folder"], config["data"]["features_filename"]
            ),
            sep="\t",
        ).drop(["Unnamed: 0"], axis=1)
        data = meta_data.merge(features, on="uuid")
    except Exception as e:
        print(f"Fail to load merged data file because of {e}")
        data = pd.DataFrame()
    return data


# Function to generate download link
def get_binary_file_downloader_html(bin_file, file_label="File"):
    with open(bin_file, "rb") as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f"data:application/octet-stream;base64,{bin_str}"
    return f'<a href="{href}" download="{file_label}">Click here to download {file_label}</a>'
