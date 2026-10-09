"""
Dataset retrieval module.

This module provides functions to fetch, download and load the
New York City Airbnb dataset from Kaggle.
"""

import os
from pathlib import Path

import kagglehub
import pandas as pd
from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DATA_DIR = _PROJECT_ROOT / "data" / "raw"
_HANDLE = "dgomonov/new-york-city-airbnb-open-data"


def get_data(force: bool = False) -> Path:
    """
    Download the dataset into data/raw/.

    Args:
        force: If True, forces download of the file even if it is
        already present.

    Returns:
        The path of the downloaded file.
    """
    _DATA_DIR.mkdir(parents=True, exist_ok=True)

    # skip download if file exists and force is False
    if not force and any(_DATA_DIR.glob("*.csv")):
        return _DATA_DIR

    # reads .env and sets the environment variables
    load_dotenv(dotenv_path=_PROJECT_ROOT / ".env")
    if not os.getenv("KAGGLE_API_TOKEN"):
        raise ValueError(
            "Kaggle credentials (KAGGLE_API_TOKEN) missing from .env file!"
        )
    downloaded_path = kagglehub.dataset_download(_HANDLE, output_dir=str(_DATA_DIR))
    return Path(downloaded_path)


def load_dataframe(filename: str = "AB_NYC_2019.csv", **kwargs) -> pd.DataFrame:
    """
    Load a CSV file from data/raw/ into a Pandas DataFrame.

    Args:
        filename: Name of the target CSV file.
        **kwargs: Additional keyword arguments passed to pd.read_csv.

    Returns:
        The loaded dataset.
    """
    data_path = get_data()
    file_path = data_path / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Could not find {filename} in {data_path}")
    return pd.read_csv(file_path, **kwargs)


if __name__ == "__main__":
    print(f"Data ready in: {get_data()}")
