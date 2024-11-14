import os
import requests
import zipfile

# Set the directory for saving downloaded files
data_dir = "./data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Function to download real estate data from Kaggle (direct download URL)
def download_real_estate_data():
    try:
        # Direct link to Kaggle dataset download (replace with the actual Kaggle dataset URL)
        kaggle_url = "https://www.kaggle.com/datasets/ahmedshahriarsakib/usa-real-estate-dataset/download"
        kaggle_zip_path = os.path.join(data_dir, "usa-real-estate-dataset.zip")

        # Request the dataset from Kaggle URL
        response = requests.get(kaggle_url)
        with open(kaggle_zip_path, 'wb') as file:
            file.write(response.content)
        
        # Extract the zip file once downloaded
        if os.path.exists(kaggle_zip_path):
            with zipfile.ZipFile(kaggle_zip_path, 'r') as zip_ref:
                zip_ref.extractall(data_dir)
            print(f"Real estate data downloaded and extracted to {data_dir}")
        else:
            print("Error: Kaggle dataset download failed or file not found.")
    
    except Exception as e:
        print(f"Error downloading the Kaggle dataset: {e}")

# Function to download NOAA climate data (direct link)
def download_noaa_climate_data():
    noaa_url = "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/mapping/110/tavg/202208/1/value"
    noaa_csv_path = os.path.join(data_dir, "noaa_climate_data.csv")
    
    try:
        # Request NOAA data from URL
        response = requests.get(noaa_url)
        response.raise_for_status()  # Ensure the request was successful
        
        with open(noaa_csv_path, 'wb') as file:
            file.write(response.content)
        print(f"NOAA climate data downloaded to {data_dir}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading NOAA data: {e}")

# Run the pipeline
def run_pipeline():
    print("Starting pipeline...")
    download_real_estate_data()
    download_noaa_climate_data()
    print("Pipeline completed successfully. Data is in the /data directory.")

if __name__ == "__main__":
    run_pipeline()
