# Code Review

## Original Code

import pandas as pd
df = pd.read_csv("daily_88101_2024.zip", compression="zip")
la = df[df["City Name"] == "Los Angeles"]
la["month"] = pd.to_datetime(la["Date Local"]).dt.month
spring = la[(la["month"] >= 3) & (la["month"] <= 5)]
result = {}
for m in [3, 4, 5]:
    vals = spring[spring["month"] == m]["Arithmetic Mean"]
    result[m] = sum(vals) / len(vals)
print(result)

## Issues with Original Code

### 1. Code filters using incorrect column

la = df[df["City Name"] == "Los Angeles"]

* The challenge instructions specify that the cities must be filtered using the CBSA Name
instead of the City Name collumn.
* This matters because filtering using City Name only will include sites with the 
exact name "Los Angeles". This method of filtering fails to represent all of the CBSA
data by not accounting for monitoring sites in the metropolitan Los Angeles.

### 2. Code is hardcoded to process data from 2024 only

df = pd.read_csv("daily_88101_2024.zip", compression="zip")

* Section 2.2 of the challenge instructions specify that monthly averages from the years 
2018-2025 must be calculated. The above code is harcoded to only process data from 2024.
* This matters because with only one year's data used, the original code does not satisfy the
challenge requirements. 

### 3. Code cannot handle invalid inputs, multiple monitoring sites, or edge cases

pd.to_datetime(la["Date Local"])

* The above code does not specify how invalid dates should be handled.
* If invalid dates are not accounted for, the entire calculation will fail. If invalid dates are
converted to NaT, they can be removed before analysis.

la = df[df["City Name"] == "Los Angeles"]
* The above code does not handle missing or empty city data. 
* This matters becauseIf there are any spelling errors or discrepancies between EPA datasets, the calculations would fail. 

la["month"] = pd.to_datetime(la["Date Local"]).dt.month

    vals = spring[spring["month"] == m]["Arithmetic Mean"]

* The above code does not account for the fact that each EPA file contains multiple monitoring sites. 
Each CBSA Name can contain multiple Arithmetic Mean rows for the same Date Local. 
* This matters because if all rows are averaged by month, without accounting for multiple
monitoring sites, dates with more reporting monitors with receive more weight, which can skew the results.

### 4. Code output is not in the required Pandas table format

    result[m] = sum(vals) / len(vals)
print(result)

* The result is an dictionary, when the challege requires months and years as collumns.
* This matters because without creating a Pandas pivot table, the project requirements are not satisfied.

## Corrected Code

### Summary of Revisions

* Processes every available annual file from 2018 onward.
* Filters using the required CBSA name.
* Reads only the necessary columns.
* Handles different ZIP archive structures.
* Cleans invalid dates and numeric values.
* Calculates one city-level mean per date.
* Calculates the March, April, and May averages from those daily values.
* Produces a table with months as rows and years as columns.

### Revised Code

from pathlib import Path
from zipfile import ZipFile

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

REQUIRED_COLUMNS = [
    "CBSA Name",
    "Date Local",
    "Arithmetic Mean",
]

MONTH_NAMES = {
    3: "March",
    4: "April",
    5: "May",
}

def load_data(year):
    file_path = DATA_DIR / f"daily_88101_{year}.zip"

    if not file_path.exists():
        raise FileNotFoundError(
            f"EPA data file was not found: {file_path}"
        )

    with ZipFile(file_path) as archive:
        csv_files = [
            name
            for name in archive.namelist()
            if name.lower().endswith(".csv")
        ]

        if not csv_files:
            raise ValueError(
                f"No CSV file was found inside {file_path.name}"
            )

        if len(csv_files) > 1:
            raise ValueError(
                f"Multiple CSV files were found inside "
                f"{file_path.name}: {csv_files}"
            )

        with archive.open(csv_files[0]) as csv_file:
            return pd.read_csv(
                csv_file,
                usecols=REQUIRED_COLUMNS,
                low_memory=False,
            )


def get_city_data(cbsa_name, year):
    df = load_data(year)

    city_df = df.loc[
        df["CBSA Name"] == cbsa_name,
        ["Date Local", "Arithmetic Mean"],
    ].copy()

    city_df["Date Local"] = pd.to_datetime(
        city_df["Date Local"],
        errors="coerce",
    )

    city_df["Arithmetic Mean"] = pd.to_numeric(
        city_df["Arithmetic Mean"],
        errors="coerce",
    )

    city_df = city_df.dropna(
        subset=["Date Local", "Arithmetic Mean"]
    )

    return city_df


def get_monthly_averages(cbsa_name):

    data_files = sorted(
        DATA_DIR.glob("daily_88101_*.zip")
    )

    records = []

    for file_path in data_files:
        year_text = file_path.stem.split("_")[-1]

        if not year_text.isdigit():
            continue

        year = int(year_text)

        if year < 2018:
            continue

        city_df = get_city_data(cbsa_name, year)

        if city_df.empty:
            continue

        city_df["Month"] = city_df["Date Local"].dt.month

        spring_df = city_df.loc[
            city_df["Month"].isin([3, 4, 5])
        ].copy()

        if spring_df.empty:
            continue

        # Produce one city-level PM2.5 value per date.
        daily_df = (
            spring_df
            .groupby(
                ["Date Local", "Month"],
                as_index=False,
            )["Arithmetic Mean"]
            .mean()
        )

        # Calculate each monthly average from the daily values.
        monthly_averages = (
            daily_df
            .groupby("Month")["Arithmetic Mean"]
            .mean()
        )

        for month_number, average in monthly_averages.items():
            records.append(
                {
                    "Year": year,
                    "Month": month_number,
                    "Average PM2.5": round(float(average), 2),
                }
            )

    if not records:
        return pd.DataFrame(
            index=list(MONTH_NAMES.values())
        )

    results = pd.DataFrame(records)

    table = results.pivot(
        index="Month",
        columns="Year",
        values="Average PM2.5",
    )

    table = table.reindex([3, 4, 5])
    table.index = table.index.map(MONTH_NAMES)

    return table


if __name__ == "__main__":
    los_angeles_cbsa = (
        "Los Angeles-Long Beach-Anaheim, CA"
    )

    result = get_monthly_averages(
        los_angeles_cbsa
    )

    print(result.to_string())