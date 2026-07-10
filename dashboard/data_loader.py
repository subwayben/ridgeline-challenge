import pandas as pd
from pathlib import Path
from zipfile import ZipFile

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
def load_data(year):
    file_path = DATA_DIR / f"daily_88101_{year}.zip"

    if not file_path.exists():
        raise FileNotFoundError(
            f"EPA data file was not found: {file_path}"
        )

    with ZipFile(file_path) as zip_file:
        csv_files = [
            name
            for name in zip_file.namelist()
            if name.lower().endswith(".csv")
        ]

        if not csv_files:
            raise ValueError(
                f"No CSV file was found inside {file_path.name}"
            )

        if len(csv_files) > 1:
            raise ValueError(
                f"Multiple CSV files were found inside {file_path.name}: "
                f"{csv_files}"
            )

        with zip_file.open(csv_files[0]) as csv_file:
            df = pd.read_csv(
                csv_file,
                low_memory=False
            )

    return df

def get_city_data(cbsa_name, year):
    df = load_data(year)

    city_df = df[df["CBSA Name"] == cbsa_name].copy()

    city_df["Date Local"] = pd.to_datetime(city_df["Date Local"])
    city_df = city_df.sort_values("Date Local")

    return city_df

def get_chart_data(cbsa_name, year):
    city_df = get_city_data(cbsa_name, year)

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

def get_monthly_averages(cbsa_name):
    month_names = {3: "March", 4: "April", 5: "May"}
    data_files = sorted(DATA_DIR.glob("daily_88101_*.zip"))
    years = []
    monthly_results = {3: {}, 4: {}, 5: {}}

    for file_path in data_files:
        year_text = file_path.stem.split("_")[-1]

        if not year_text.isdigit():
            continue

        year = int(year_text)

        # The challenge begins with 2018.
        if year < 2018:
            continue

        city_df = get_city_data(cbsa_name, year)

        if city_df.empty:
            continue

        # Add a numeric month column.
        city_df["Month"] = city_df["Date Local"].dt.month

        # Keep only March, April, and May.
        spring_df = city_df[city_df["Month"].isin([3, 4, 5])]

        # First calculate one mean per date. This prevents days with more
        # monitoring sites from receiving more weight than other days.
        daily_df = (
            spring_df
            .groupby(["Date Local", "Month"], as_index=False)["Arithmetic Mean"]
            .mean()
        )

        # Then calculate the average of the daily values for each month.
        month_averages = (
            daily_df
            .groupby("Month")["Arithmetic Mean"]
            .mean()
        )

        years.append(year)

        for month_number in [3, 4, 5]:
            if month_number in month_averages.index:
                monthly_results[month_number][year] = float(
                round(month_averages.loc[month_number], 2)
)
            else:
                monthly_results[month_number][year] = None

    years = sorted(set(years))

    rows = []

    for month_number in [3, 4, 5]:
        rows.append({
            "month": month_names[month_number],
            "values": [
                monthly_results[month_number].get(year)
                for year in years
            ],
        })

    return {
        "years": years,
        "rows": rows,
    }
