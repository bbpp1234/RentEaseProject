import os

# Get the absolute path to the project root
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directories
DOWNLOAD_DIR = '.'
PROCESSED_DIR = '.'
FINAL_DIR = '.'
FACILITIES_EXTRACT_DIR = '.'

# File names for datasets
ZIP_FILE_NAME = "facilities.zip"
FACILITIES_FILE_NAME = 'facilities_24v1.csv'
APARTMENT_DATA_FILE = 'apartment_data_raw.csv'
PREDOWNLOAD_APARTMENT_DATA_FILE = '[predownload]apartment_data_raw.csv'
PROCESSED_APARTMENT_DATA_FILE = 'apartment_data_processed.csv'
SHOOTING_FILE_NAME = "shooting_data.csv"
COMPLAINT_FILE_NAME = "complaint_data.csv"
MERGED_DATA = 'final_grouped_apartment_data_with_pivot.csv'

# Full paths
APARTMENT_DATA_PATH = os.path.join(DOWNLOAD_DIR, APARTMENT_DATA_FILE)
PREDOWNLOAD_APARTMENT_DATA_PATH= os.path.join(DOWNLOAD_DIR, PREDOWNLOAD_APARTMENT_DATA_FILE)
PROCESSED_APARTMENT_DATA_PATH = os.path.join(DOWNLOAD_DIR, PROCESSED_APARTMENT_DATA_FILE) 
FACILITIES_DATA_PATH = os.path.join(FACILITIES_EXTRACT_DIR, FACILITIES_FILE_NAME)
SHOOTING_DATA_PATH = os.path.join(DOWNLOAD_DIR, SHOOTING_FILE_NAME)
MERGED_DATA_PATH = os.path.join(PROCESSED_DIR, MERGED_DATA)
