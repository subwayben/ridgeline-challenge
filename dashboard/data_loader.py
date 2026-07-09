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

def get_chart_data(cbsa_name):
    city_df = get_city_data(cbsa_name)

    daily_df = (
        city_df
        .groupby("Date Local", as_index=False)["Arithmetic Mean"]
        .mean()
        .sort_values("Date Local")
    )

    dates = daily_df["Date Local"].dt.strftime("%Y-%m-%d").tolist()
    values = daily_df["Arithmetic Mean"].round(2).tolist()

    return {
        "dates": dates,
        "values": values,
    }

from dashboard.data_loader import load_data

df = load_data()

df.head()