# %%
# File: apartment_filter.py
# Group members: rivenl, leylal, chengkac, bangminp

# This script filters apartment data based on user preferences (query parameters) 
# and selected facilities. It outputs the filtered results to a CSV file with a timestamp.
# This file imports configuration settings from the `config.py` module and uses the 
# `timestamp.py` module to generate a timestamped filename for the output.
# The code dynamically filters the DataFrame rows and selected columns for facilities.

import pandas as pd
import os
import sys
sys.path.append('./')  # Add current directory to sys.path
from config import *
import timestamp as timestamp


def filter_dataframe(query_params, facilities):
    """
    Apply dynamic filters to the DataFrame based on query parameters.
    For Facilities, only keep selected columns.
    :param query_params: Dictionary where keys are column names and values are filter conditions.
    :param facilities: List of selected facility column names for filtering columns.
    :return: Filtered DataFrame with only selected facility columns.
    """
    file_path = os.path.join(PROCESSED_DIR, MERGED_DATA)
    df = pd.read_csv(file_path)

    # Make sure columns like 'Average Rent' are numeric
    df['AVERAGE RENT'] = pd.to_numeric(df['AVERAGE RENT'], errors='coerce')

    # Construct query string for row filtering based on query_params
    query_string = " & ".join(
        [
            f"`{col}` {op} '{vals[0]}'" if isinstance(vals[0], str) else f"`{col}` {op} {vals[0]}"
            if len(vals) == 1 else f"(`{col}` >= {vals[0]} & `{col}` <= {vals[1]})"
            for col, condition in query_params.items() if condition is not None
            for op, *vals in [condition]  # Unpack operator and value(s)
        ]
    )

    # Print the generated query string for debugging
    print(f"Generated query string: {query_string}")

    # If there is a valid query string, apply it
    if query_string:
        try:
            # Use the 'python' engine to bypass numexpr issues
            filtered_df = df.query(query_string, engine='python')
        except Exception as e:
            print(f"Error applying query: {query_string}")
            raise e
    else:
        filtered_df = df  # No filtering, keep all rows if no conditions were specified

    # For Facilities, only keep the columns the user selected
    if facilities:
        # Ensure we don't lose the core columns (like Address, Rent, etc.)
        base_columns = ['ADDRESS', 'APARTMENT NAME', 'AVERAGE RENT', 'ZIP CODE', 'CITY']
        # Add facility columns to the base columns
        selected_columns = base_columns + facilities
        filtered_df = filtered_df[selected_columns]

    print(f"Selected columns: {selected_columns}")
    print(f"{len(filtered_df)} apartments match your preferences.")
    return filtered_df

def to_csv_with_timestamp(filtered_df):
    stamp = timestamp.generate_timestamp()
    file_path = f"{FINAL_DIR}/[{stamp}]recommendation_for_user.csv"
    
    # The columns to keep for final output
    # keep_columns = ['Address','Apartment Name','Rent','Features','ZIP Code','City']
    # filtered_df = filtered_df[keep_columns]
    
    filtered_df.to_csv(file_path, index = False)
    print(f"The recommended list is output to {file_path}")

if __name__ == "__main__":
    # Example query parameters for filtering (user preferences)
    query_params = {
    'AVERAGE RENT': ('between', 2000, 2800),
    'IF_PETS_ALLOWED': ('==', 'Allowed'),
    'Safety_level': ('==', 'Caution Advised')
}

    facilities = ['BUS STATION', 'MUSEUM']  # Multiple facilities selected

    # Call the filter_dataframe function with the above inputs
    filtered_df = filter_dataframe(query_params, facilities)
