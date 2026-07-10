# Ridgeline Air Pollution Data Dashboard

A Django web application that analyzes and visualizes daily PM2.5 air-pollution data from the EPA.

The dashboard displays an interactive map of the United States with markers for:

* Los Angeles, California
* San Diego, California
* New York City, New York

Selecting a city opens a page containing:

* A time-series chart of daily PM2.5 values
* A table of average PM2.5 values for March, April, and May
* Monthly results for each available year from 2018 onward

## Technologies Used

* Python
* Django
* Pandas
* Bootstrap
* Leaflet
* Chart.js
* EPA AirData daily summary files

## Data Source

The application uses the EPA’s pre-generated daily summary files for PM2.5 parameter code `88101`.

The files follow this naming format:

```text
daily_88101_<YEAR>.zip
```

The application filters the EPA data using the `CBSA Name` column and uses the following columns for analysis:

* `Date Local`
* `Arithmetic Mean`

Because some ZIP archives have different internal folder structures, the application searches each archive for its CSV file before loading it with Pandas.

The 2024 EPA file identifies the San Diego metropolitan area as:

```text
San Diego-Carlsbad, CA
```

This differs from the longer CBSA name listed in the challenge instructions, so the application uses the value found in the dataset.

## Project Structure

```text
ridgeline_challenge/
├── dashboard/
│   ├── templates/
│   │   └── dashboard/
│   │       ├── home.html
│   │       └── city.html
│   ├── data_loader.py
│   ├── urls.py
│   └── views.py
├── data/
│   ├── daily_88101_2018.zip
│   ├── daily_88101_2019.zip
│   ├── daily_88101_2020.zip
│   ├── daily_88101_2021.zip
│   ├── daily_88101_2022.zip
│   ├── daily_88101_2023.zip
│   ├── daily_88101_2024.zip
│   └── daily_88101_2025.zip
├── pollution_dashboard/
├── manage.py
├── requirements.txt
├── code_review.md
├── AI_USAGE.md
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <https://github.com/subwayben/ridgeline-challenge>
cd ridgeline_challenge
```

### 2. Create a virtual environment

On macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the EPA data files

Create a folder named `data` in the project root.

Download the EPA PM2.5 daily summary ZIP files and place them in that folder using the following filename format:

```text
daily_88101_<YEAR>.zip
```

The application processes files from 2018 onward and automatically detects available years.

### 5. Apply Django migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open the following address in a web browser:

```text
http://127.0.0.1:8000/
```

## How the Application Works

The homepage uses Leaflet to display an interactive map with markers for the three required metropolitan areas.

When a city is selected:

1. Django routes the request to the city view.
2. Pandas reads the appropriate EPA ZIP file.
3. The data is filtered using the city’s CBSA name.
4. Measurements from multiple monitoring sites are averaged to produce one value per date.
5. Chart.js displays the daily values as a time-series graph.
6. Pandas calculates March, April, and May averages for every available year.
7. Django renders those averages in a Bootstrap table.

## Notes

The application reads several large EPA files when a city page is opened. As a result, the first page load may take several seconds.

This application uses Django’s development server and is intended for local demonstration and evaluation rather than production deployment.

