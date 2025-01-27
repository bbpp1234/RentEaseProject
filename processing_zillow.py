#%%
# File: processing_zillow.py
# Group members: rivenl, leylal, chengkac, bangminp

# This script processes apartment raw data scraped from Zillow. It includes functions to clean the data,
# extract useful information like ZIP code, city, and borough, and calculate average rent.
# It also handles pet policy information and outputs a cleaned DataFrame with necessary columns for further analysis.


import pandas as pd


def process_apartment_data(df):
    # Drop rows where 'Address' is NaN
    df = df.dropna(subset=['Address'])

    # Extract the ZIP code (last 5 characters in 'Address')
    df['ZIP Code'] = df['Address'].str[-5:]

    # Extract the city name (string between the first and second comma)
    df['City'] = df['Address'].str.split(',').str[1].str.strip()

    # Define boroughs and their corresponding ZIP code ranges
    boroughs = {
        "MANHATTAN": range(10001, 10283),
        "BROOKLYN": range(11201, 11257),
        "QUEENS": list(range(11001, 11437)) + list(range(11691, 11698)),
        "BRONX": range(10451, 10476),
        "STATEN ISLAND": range(10301, 10315)
    }

    # Function to determine borough based on ZIP code
    def find_borough(zip_code):
        try:
            zip_code = int(zip_code)  # Convert ZIP code to integer
            for borough, zip_range in boroughs.items():
                if zip_code in zip_range:
                    return borough
        except ValueError:
            return "Unknown"
        return "Unknown"

    # Apply the find_borough function to create the BORO column
    df['BORO'] = df['ZIP Code'].apply(find_borough)

    def calculate_average_rent(rent):
        if pd.isna(rent) or not isinstance(rent, str):
            return None

        # Remove any dollar signs, commas, /mo, and split the range
        rent_range = rent.replace('$', '').replace('/mo', '').replace(',', '').replace('+', '').split('-')

        # Handle case where the rent contains non-numeric values (like 'N/A')
        try:
            if len(rent_range) == 2:  # If it's a range, calculate the average
                average_rent = (int(rent_range[0].strip()) + int(rent_range[1].strip())) / 2
                return average_rent
            elif len(rent_range) == 1:  # If it's a single value, return it as an integer
                return int(rent_range[0].strip())
        except ValueError:
            # Return None if there's any issue converting to int (e.g., if rent is 'N/A')
            return None

        return None

    df['Average Rent'] = df['Rent'].apply(calculate_average_rent)

    def process_pet_policy(row):
        if 'Allowed' in str(row['Dogs Policy']) or 'Allowed' in str(row['Cats Policy']) or 'Allowed' in str(row['Large Dogs Policy']) or 'Allowed' in str(row['Small Dogs Policy']):
            return 'Allowed'
        elif 'Yes' in str(row['Pets Allowed']):
            return 'Allowed'
        elif 'Not allowed' in str(row['Dogs Policy']) or 'Not allowed' in str(row['Cats Policy']) or 'Not allowed' in str(row['Large Dogs Policy']) or 'Not allowed' in str(row['Small Dogs Policy']):
            return 'Not Allowed'
        elif 'No' in str(row['Pets Allowed']):
            return 'Not Allowed'
        else:
            return 'N/A'

    df['If_Pets_Allowed'] = df.apply(process_pet_policy, axis=1)

    # Explicitly assigning the result to avoid the view vs. copy warning
    df = df.drop(columns=['Dogs Policy', 'Cats Policy', 'Large Dogs Policy', 'Small Dogs Policy', 'Pets Allowed'])

    return df
