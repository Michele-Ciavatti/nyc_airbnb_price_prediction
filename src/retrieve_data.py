from dotenv import load_dotenv
import os
from pathlib import Path
import pandas as pd
import kagglehub

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
HANDLE = "dgomonov/new-york-city-airbnb-open-data"

def get_data(force: bool = False) -> Path:
    """Download the dataset into data/ unsless it's already there."""
    DATA_DIR.mkdir(parents = True, exist_ok = True)

    # skip download if file exists and force is False
    if not force and any(DATA_DIR.glob("*.csv")):
        return DATA_DIR

    load_dotenv(dotenv_path = PROJECT_ROOT / ".env") # reads .env and sets the environment variables
    if not os.getenv("KAGGLE_API_TOKEN"):
        raise ValueError(
            "Kaggle credentials (KAGGLE_API_TOKEN) missing from .env file!"
        )
    downloaded_path = kagglehub.dataset_download(HANDLE, output_dir = str(DATA_DIR))
    return Path(downloaded_path)

def load_dataframe(filename: str = "AB_NYC_2019.csv", **kwargs) -> pd.DataFrame:
    data_path = get_data()
    file_path = data_path / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Could not find {filename} in {data_path}")
    return pd.read_csv(file_path, **kwargs)

if __name__ == "__main__": print(f"Data ready in: {get_data()}")