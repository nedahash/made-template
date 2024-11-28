import os
import pandas as pd
import requests
import sqlite3

# Directory setup
DATA_DIR = "/data"
os.makedirs(DATA_DIR, exist_ok=True)

# Data sources
EIA_URL = "https://www.eia.gov/environment/emissions/state/excel/table1.xlsx"
EIA_FILE = f"{DATA_DIR}/eia_emissions.xlsx"
COVID_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv"
COVID_FILE = f"{DATA_DIR}/covid_cases.csv"
DB_FILE = f"{DATA_DIR}/combined_data.db"

def download_file(url, file_path):
    """Download a file from the given URL."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded: {file_path}")
    else:
        raise Exception(f"Failed to download file from {url}")

def process_eia_data(file_path):
    """Process the EIA emissions data."""
    # Load the Excel file
    data = pd.read_excel(file_path, sheet_name=0, skiprows=4)
    print("EIA Columns:", data.columns)

    # Rename columns for consistency
    data.rename(columns={
        "State": "state",
        "Carbon Dioxide (CO2) Emissions (million metric tons)": "co2_emissions"
    }, inplace=True)

    # Filter out irrelevant rows (e.g., footnotes or total rows)
    data = data.dropna(subset=["state", "co2_emissions"])

    # Convert data types
    data["co2_emissions"] = pd.to_numeric(data["co2_emissions"], errors="coerce")

    return data[["state", "co2_emissions"]]

def process_covid_data(file_path):
    """Process the COVID-19 cases data."""
    # Load the CSV file
    data = pd.read_csv(file_path)
    print("COVID Columns:", data.columns)

    # Select relevant columns
    data = data[["state", "cases", "deaths"]]

    # Handle missing values
    data["cases"] = data["cases"].fillna(0).astype(int)
    data["deaths"] = data["deaths"].fillna(0).astype(int)

    return data

def merge_data(eia_data, covid_data):
    """Merge EIA emissions data and COVID-19 cases data."""
    merged = pd.merge(eia_data, covid_data, on="state", how="inner")
    return merged

def save_to_database(data, db_path, table_name):
    """Save the merged data to an SQLite database."""
    conn = sqlite3.connect(db_path)
    data.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Data saved to database: {db_path}, table: {table_name}")

def main():
    print("Starting pipeline...")

    # Step 1: Download datasets
    print("Downloading EIA emissions data...")
    download_file(EIA_URL, EIA_FILE)

    print("Downloading COVID-19 cases data...")
    download_file(COVID_URL, COVID_FILE)

    # Step 2: Process datasets
    print("Processing EIA emissions data...")
    eia_data = process_eia_data(EIA_FILE)

    print("Processing COVID-19 cases data...")
    covid_data = process_covid_data(COVID_FILE)

    # Step 3: Merge datasets
    print("Merging datasets...")
    merged_data = merge_data(eia_data, covid_data)

    # Step 4: Save merged data to database
    print("Saving merged data to database...")
    save_to_database(merged_data, DB_FILE, "eia_covid_data")

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
