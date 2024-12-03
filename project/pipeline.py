import os
import pandas as pd
import requests
import sqlite3

# Directory setup
DATA_DIR = "./data"
os.makedirs(DATA_DIR, exist_ok=True)

# Data sources
EIA_URL = "https://www.eia.gov/environment/emissions/state/excel/table1.xlsx"
EIA_FILE = f"{DATA_DIR}/eia_emissions.xlsx"
COVID_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv"
COVID_FILE = f"{DATA_DIR}/covid_cases.csv"
DB_FILE = f"{DATA_DIR}/combined_data.db"


def download_file(url, file_path):
    """Download a file from the given URL."""
    try:
        print(f"Downloading from: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded successfully: {file_path}")
        else:
            raise Exception(f"Failed to download file. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading file {file_path}: {e}")
        raise


def process_eia_data(file_path):
    """Process the EIA emissions data."""
    try:
        print(f"Processing EIA data from: {file_path}")
        data = pd.read_excel(file_path, sheet_name=0, skiprows=4)
        print("EIA Raw Columns:", data.columns)

        # Detect the latest year column dynamically
        year_columns = [col for col in data.columns if isinstance(col, (int, str)) and str(col).isdigit()]
        if not year_columns:
            raise ValueError("No numeric year columns found in the EIA dataset.")
        latest_year = max(year_columns, key=lambda x: int(x))
        print(f"Using emissions data for the year: {latest_year}")

        # Keep only the 'State' column and the latest year column
        if "State" not in data.columns:
            raise KeyError("The 'State' column is missing from the EIA data.")
        filtered_data = data[["State", latest_year]].rename(columns={"State": "state", latest_year: "co2_emissions"})

        # Remove rows with missing values in 'state' or 'co2_emissions'
        filtered_data = filtered_data.dropna(subset=["state", "co2_emissions"])

        # Convert 'co2_emissions' to numeric, coercing invalid values to NaN
        filtered_data["co2_emissions"] = pd.to_numeric(filtered_data["co2_emissions"], errors="coerce")

        # Drop rows with invalid 'co2_emissions'
        filtered_data = filtered_data.dropna(subset=["co2_emissions"])

        print("Processed EIA Data Sample:")
        print(filtered_data.head())
        return filtered_data
    except Exception as e:
        print(f"Error processing EIA data: {e}")
        raise


def process_covid_data(file_path):
    """Process the COVID-19 cases data."""
    try:
        print(f"Processing COVID data from: {file_path}")
        data = pd.read_csv(file_path)
        print("COVID Raw Columns:", data.columns)

        # Select relevant columns
        data = data[["state", "cases", "deaths"]]

        # Handle missing values
        data["cases"] = data["cases"].fillna(0).astype(int)
        data["deaths"] = data["deaths"].fillna(0).astype(int)

        print("Processed COVID Data Sample:")
        print(data.head())
        return data
    except Exception as e:
        print(f"Error processing COVID data: {e}")
        raise


def merge_data(eia_data, covid_data):
    """Merge EIA emissions data and COVID-19 cases data."""
    try:
        print("Merging datasets...")
        merged = pd.merge(eia_data, covid_data, on="state", how="inner")
        print(f"Merged Data Sample:")
        print(merged.head())
        return merged
    except Exception as e:
        print(f"Error merging data: {e}")
        raise


def save_to_database(data, db_path, table_name):
    """Save the merged data to an SQLite database."""
    try:
        print(f"Saving data to database: {db_path}, table: {table_name}")
        conn = sqlite3.connect(db_path)
        data.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.close()
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data to database: {e}")
        raise


def main():
    try:
        print("Starting pipeline...")

        # Step 1: Download datasets
        print("Step 1: Downloading EIA emissions data...")
        download_file(EIA_URL, EIA_FILE)

        print("Step 1: Downloading COVID-19 cases data...")
        download_file(COVID_URL, COVID_FILE)

        # Step 2: Process datasets
        print("Step 2: Processing EIA emissions data...")
        eia_data = process_eia_data(EIA_FILE)
        print("Step 2: Processing COVID-19 cases data...")
        covid_data = process_covid_data(COVID_FILE)

        # Step 3: Merge datasets
        print("Step 3: Merging datasets...")
        merged_data = merge_data(eia_data, covid_data)

        # Step 4: Save merged data to database
        print("Step 4: Saving merged data to database...")
        save_to_database(merged_data, DB_FILE, "eia_covid_data")

        print("Pipeline completed successfully!")
    except Exception as e:
        print(f"Pipeline failed: {e}")


if __name__ == "__main__":
    main()
