#%%
# File: shooting_crawler.py
# Group members: rivenl, leylal, chengkac, bangminp

# This file fetches shooting incident data from NYC's open data API using Socrata.
# It retrieves the data, converts it into a pandas DataFrame, and saves it to a CSV file.
# The main modules imported by this file are `os`, `pandas`, and `sodapy`.
# It imports constants `DOWNLOAD_DIR` and `SHOOTING_FILE_NAME` from `config.py`.
# This script can be run independently to download and save the latest data.

# Make sure to install these packages before running:
# pip install pandas
# pip install sodapy


import os
import pandas as pd
from sodapy import Socrata
from config import *  

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cityofnewyork.us", None)

def fetch_shooting_data(download_dir, file_name, limit=999999999):
    """Fetches shooting incident data from the NYC open data API."""

    predownload_or_not = input("It takes less than one minute to scrape fresh apartment data.\n"
                               "Use predownloaded shooting data? (y/n): ").strip().lower()

    if predownload_or_not == "y" and os.path.exists(os.path.join(download_dir, file_name)):
        print("Loading predownloaded shooting data...")
        return pd.read_csv(os.path.join(download_dir, file_name))
    else:
        print("Downloading fresh shooting data from the API...")
        try:
            # Fetch the data from the API
            results = client.get("833y-fsy8", limit=limit)

            # Convert to pandas DataFrame
            results_df = pd.DataFrame.from_records(results)

            # Save the DataFrame to a CSV file
            file_path = os.path.join(download_dir, file_name)
            results_df.to_csv(file_path, index=False)

            print(f"Shooting incident data is saved to {file_path}")
            print(f'{len(results_df)} records are downloaded')

            return results_df  # Return the DataFrame if needed
        except Exception as e:
            print(f"An error occurred while fetching data: {e}")
            return None

def run_crawler():
    """Main function to run the shooting incidents data crawler."""
    fetch_shooting_data(DOWNLOAD_DIR, SHOOTING_FILE_NAME)

if __name__ == "__main__":
    run_crawler()
# %%
