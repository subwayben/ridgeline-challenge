import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FILE_PATH = DATA_DIR / "daily_88101_2024.zip"
def load_data():
    df = pd.read_csv(FILE_PATH, compression="zip")
    return df

from dashboard.data_loader import load_data

df = load_data()

df.head()