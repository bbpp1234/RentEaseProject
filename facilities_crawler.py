#%%
# File: facilities_crawler.py
# Group members: rivenl, leylal, chengkac, bangminp

# This file downloads a zip file containing NYC facility data, extracts its contents, 
# and saves it to a specified directory. It uses `requests` to download the file 
# and `zipfile` to extract it.
# The script imports constants like `DOWNLOAD_DIR`, `ZIP_FILE_NAME`, and `FACILITIES_EXTRACT_DIR`
# from the `config.py` module. This file can be run independently.


import requests
import zipfile
import os
from config import *

#%%
# URL of the zip file
URL = "https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/facilities_24v1_csv.zip"


def download_file(url, download_dir, file_name):
    """Downloads a file from the specified URL to the given directory."""
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)  # Create directory if it doesn't exist
    file_path = os.path.join(download_dir, file_name)

    print(f"Downloading {file_name}...")
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors

    with open(file_name, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {file_name}")

    return file_name

def extract_zip(zip_file_path, extract_dir):
    """Extracts the contents of a zip file to the specified directory."""
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)  # Create directory if it doesn't exist

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print("Extracted contents ")

def run_crawler():
    """Main function to run the facilities data crawler, with an option for using predownloaded data."""
    
    predownload_or_not = input("It takes less than one minute to scrape fresh facilities data.\n"
                               "Do you want to use predownloaded facilities data? (y/n): ").strip().lower()
    
    predownloaded_zip_path = os.path.join(DOWNLOAD_DIR, ZIP_FILE_NAME)

    # Use predownloaded data if available and chosen
    if predownload_or_not == "y" and os.path.exists(predownloaded_zip_path):
        print(f"Loading predownloaded facilities data from {predownloaded_zip_path}")
        extract_zip(predownloaded_zip_path, FACILITIES_EXTRACT_DIR)
    else:
        print("Downloading fresh facilities data from the web...")
        # Download and extract fresh data
        zip_file_path = download_file(URL, DOWNLOAD_DIR, ZIP_FILE_NAME)
        extract_zip(zip_file_path, FACILITIES_EXTRACT_DIR)

if __name__ == "__main__":
    run_crawler()
