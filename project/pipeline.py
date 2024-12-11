import os
import pandas as pd
import requests
import sqlite3

# Directory setup
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
os.makedirs(DATA_DIR, exist_ok=True)

# Data sources
EIA_URL = "https://www.eia.gov/environment/emissions/state/excel/table1.xlsx"
EIA_FILE = os.path.join(DATA_DIR, "eia_emissions.xlsx")
COVID_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv"
COVID_FILE = os.path.join(DATA_DIR, "covid_cases.csv")
DB_FILE = os.path.join(DATA_DIR, "combined_data.db")


def download_file(url, file_path):
    """Download a file from the given URL."""
    if not os.path.exists(file_path):
        print(f"Downloading from: {url}")
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded successfully: {file_path}")
    else:
        print(f"File already exists: {file_path}")


def process_eia_data(file_path):
    """Process the EIA emissions data."""
    data = pd.read_excel(file_path, sheet_name=0, skiprows=4)
    year_columns = [col for col in data.columns if isinstance(col, (int, str)) and str(col).isdigit()]
    latest_year = max(year_columns, key=lambda x: int(x))
    filtered_data = data[["State", latest_year]].rename(columns={"State": "state", latest_year: "co2_emissions"}).dropna()
    filtered_data["co2_emissions"] = pd.to_numeric(filtered_data["co2_emissions"], errors="coerce").dropna()
    return filtered_data


def process_covid_data(file_path):
    """Process the COVID-19 cases data."""
    data = pd.read_csv(file_path)[["state", "cases", "deaths"]]
    data["cases"] = data["cases"].fillna(0).astype(int)
    data["deaths"] = data["deaths"].fillna(0).astype(int)
    return data


def merge_data(eia_data, covid_data):
    """Merge EIA emissions data and COVID-19 cases data."""
    return pd.merge(eia_data, covid_data, on="state", how="inner")


def save_to_database(data, db_path, table_name):
    """Save the merged data to an SQLite database."""
    conn = sqlite3.connect(db_path)
    data.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()


def main():
    download_file(EIA_URL, EIA_FILE)
    download_file(COVID_URL, COVID_FILE)
    eia_data = process_eia_data(EIA_FILE)
    covid_data = process_covid_data(COVID_FILE)
    merged_data = merge_data(eia_data, covid_data)
    save_to_database(merged_data, DB_FILE, "eia_covid_data")


if __name__ == "__main__":
    main()
