#%%
# File: interactive_page.py
# Group members: rivenl, leylal, chengkac, bangminp

# This script collects user preferences for apartment searches and filters data based on the input.
# The user is prompted to enter their preferred borough, price range, pet policy, school grade,
# desired nearby facilities, and crime safety level. 
# The collected preferences are then stored in `query_params` and `facilities` for filtering the dataset later.


import pandas as pd
import numpy as np
import sys
sys.path.append('./')  # Add current directory to sys.path
from config import PROCESSED_APARTMENT_DATA_PATH, FACILITIES_DATA_PATH, SHOOTING_DATA_PATH, MERGED_DATA_PATH

def merge_datasets_with_pivot():
    """Merge processed apartment data with facilities and shooting data, and create a pivot table."""

    # Load the processed apartment data
    apartment_data = pd.read_csv(PROCESSED_APARTMENT_DATA_PATH)
    print(f"Apartment data loaded with shape: {apartment_data.shape}\n")

    # Load and filter facilities data
    facilities_data = pd.read_csv(FACILITIES_DATA_PATH, usecols=['FACTYPE', 'BORO'])
    print(f"Facilities data loaded with shape: {facilities_data.shape}")

    # Filter based on FACTYPE
    valid_factypes = ['BUS STATION', 'MUSEUM', 'COMMERCIAL GARAGE AND PARKING LOT', 'PUBLIC LIBRARY']
    facilities_data = facilities_data[facilities_data['FACTYPE'].isin(valid_factypes)]
    print(f"Facilities data shape after filtering: {facilities_data.shape}\n")

    # Step 1: Merge Property and Facility Data
    # Ensure consistent naming for 'BORO' across all datasets
    apartment_data.columns = apartment_data.columns.str.upper()
    facilities_data.columns = facilities_data.columns.str.upper()
    print("Column names standardized.\n")

    # Merge apartment data with facilities data on 'BORO'
    merged_apartment_facilities = pd.merge(apartment_data, facilities_data, on='BORO', how='left')
    print(f"Merged data shape: {merged_apartment_facilities.shape}\n")

    # Step 2 Pivot Facility Data to return to 119 rows
    # Index by apartment address
    print("Creating pivot table from merged data...")
    pivot_table = pd.pivot_table(
        merged_apartment_facilities,
        index=['ADDRESS'],
        columns='FACTYPE',
        aggfunc='size',
        fill_value=0
    ).reset_index()
    print(f"Pivot table created with shape: {pivot_table.shape}\n")

    # Merge the pivot table back to the apartment data
    final_data = pd.merge(apartment_data, pivot_table, on='ADDRESS', how='left')
    print(f"Final data shape after merging with pivot table: {final_data.shape}\n")

    # Fill NaN values with zeros for facility counts
    facility_columns = valid_factypes
    final_data[facility_columns] = final_data[facility_columns].fillna(0)

    # Step 3 Merge with Shooting Incident Data
    shooting_data = pd.read_csv(SHOOTING_DATA_PATH, usecols=['boro'])
    print(f"Shooting data loaded with shape: {shooting_data.shape}\n")
    shooting_data.columns = shooting_data.columns.str.upper()

    # Merge apartment data with shooting data on 'BORO'
    final_data = pd.merge(final_data, shooting_data.drop_duplicates(), on='BORO', how='left', indicator=True)
    print(f"Final data shape after merging with shooting data: {final_data.shape}\n")

    # Add Safety_level column based on BORO
    conditions = [
        (final_data['BORO'] == 'BROOKLYN'),
        (final_data['BORO'] == 'QUEENS'),
        (final_data['BORO'] == 'BRONX'),
        (final_data['BORO'] == 'MANHATTAN')
    ]

    # Values to assign for each condition
    values = ['Caution Advised', 'Relatively Safe', 'Relatively Safe', 'Very Safe']

    # Create the new column 'Safety_level' using np.select
    final_data['Safety_level'] = np.select(conditions, values, default='Unknown')
    print("'Safety_level' column added.\n")

    # Save the final merged dataset
    final_data.to_csv(MERGED_DATA_PATH, index=False)
    print("Final merged dataset saved successfully.")
