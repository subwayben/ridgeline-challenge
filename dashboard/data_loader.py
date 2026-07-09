import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FILE_PATH = DATA_DIR / "daily_88101_2024.zip"


def load_data():
    df = pd.read_csv(FILE_PATH, compression="zip", low_memory=False)
    return df


def get_city_data(cbsa_name):
    df = load_data()

    city_df = df[df["CBSA Name"] == cbsa_name].copy()

    city_df["Date Local"] = pd.to_datetime(city_df["Date Local"])
    city_df = city_df.sort_values("Date Local")

    return city_df
