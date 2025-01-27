# File: main.py
# Group members: rivenl, leylal, chengkac, bangminp

# This file coordinates the apartment recommendation pipeline by calling various modules.
# It fetches data from multiple sources (e.g., facilities, shooting incidents), processes apartment data,
# merges datasets, applies user-defined filters, and saves the final recommendation list to a CSV file.
# It imports modules like `facilities_crawler`, `shooting_crawler`, `apartment_crawler`, `processing_zillow`, 
# `merger`, `interactive_page`, and `data_filter`. The file also imports configuration constants from `config.py`.
# This script should be run to perform the full end-to-end apartment recommendation process.

from config import *
import pandas as pd
import facilities_crawler 
import shooting_crawler 
# import complaint_crawler 
import apartment_crawler

import processing_zillow
import merger
import interactive_page
import data_filter 


# %%
def main():
    # Step 0: Download source data
    print("Running facilities crawler...")
    facilities_crawler.run_crawler()
    
    print("Running shooting data crawler...")
    shooting_crawler.run_crawler()

    # Step 1: Load the raw apartment data
    print("Scraping apartment data...")
    apartment_df = apartment_crawler.scrape_apartment_data()
    
    # Step 2: Process the apartment data
    print("Processing apartment data...")
    processed_apartment_data = processing_zillow.process_apartment_data(apartment_df)

    # Step 3: Save the processed apartment data to the processed folder
    print("Saving processed apartment data...")
    processed_apartment_data.to_csv(PROCESSED_APARTMENT_DATA_PATH, index=False)

    # Step 4: Merge the processed apartment data with facilities and shooting data
    print("Merging datasets...")
    merger.merge_datasets_with_pivot()

    # Step 5: Collect user preferences
    print("Collecting user preferences...")
    query_params, facilities = interactive_page.collect_preferences()

    # Step 6: Filter the data based on user input
    print("Filtering the dataset...")
    filtered_df = data_filter.filter_dataframe(query_params, facilities)
    
    # Step 7: Save the filtered data with a timestamp
    print("Saving filtered dataset...")
    data_filter.to_csv_with_timestamp(filtered_df)

if __name__ == "__main__":
    main()
