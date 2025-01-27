#%%
# File: interactive_page.py
# Group members: rivenl, leylal, chengkac, bangminp

# This script presents an interactive page to collect user preferences for filtering apartment data.
# The user is prompted to enter their preferences regarding borough, price range, pet policy, school grade, 
# facilities nearby, and crime level. Based on the input, the script builds a dictionary `query_params` to 
# filter apartment data and a list of `facilities` to filter facility columns.
# The collected preferences are returned for further use in filtering apartment data.


# Define options
borough_options = ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'Not to matter']
price_range_options = ['< 2000', '2000-2800', '2800-3600', '3600-4400', '> 4400', 'Not to matter']
pet_policy_options = ['Yes', 'No', 'Not to matter']  # 'Yes' means 'Allowed', 'No' means 'Not Allowed'
facilities_options = ['BUS STATION', 'MUSEUM', 'COMMERCIAL GARAGE AND PARKING LOT', 'PUBLIC LIBRARY', 'Not to matter']
crime_options = ['Caution Advised', 'Relatively Safe', 'Very Safe', 'Not to matter']

def collect_preferences():
    """
    Collect user preferences and return two outputs:
    - query_params: A dictionary of filtering conditions for row filtering.
    - facilities: A list of selected facility column names for filtering columns.
    """
    query_params = {}  # Initialize empty dictionary for filters
    
    # Asking for Borough
    print("\nWhich borough would you like to live in? (Enter number)")
    for idx, option in enumerate(borough_options):
        print(f"{idx + 1}. {option}")
    boro_choice = int(input()) - 1
    if borough_options[boro_choice] != 'Not to matter':
        query_params['BORO'] = ('==', borough_options[boro_choice])

    # Asking for Price Range
    print("\nWhat's your price range preference? (Enter number)")
    for idx, option in enumerate(price_range_options):
        print(f"{idx + 1}. {option}")
    price_choice = int(input()) - 1

    # Handling Average Rent based on the selected range
    if price_range_options[price_choice] == '< 2000':
        query_params['AVERAGE RENT'] = ('<', 2000)
    elif price_range_options[price_choice] == '2000-2800':
        query_params['AVERAGE RENT'] = ('between', 2000, 2800)
    elif price_range_options[price_choice] == '2800-3600':
        query_params['AVERAGE RENT'] = ('between', 2800, 3600)
    elif price_range_options[price_choice] == '3600-4400':
        query_params['AVERAGE RENT'] = ('between', 3600, 4400)
    elif price_range_options[price_choice] == '> 4400':
        query_params['AVERAGE RENT'] = ('>', 4400)

    # Asking for Pet Policy
    print("\nDo you require pet-friendly apartments? (Enter number)")
    for idx, option in enumerate(pet_policy_options):
        print(f"{idx + 1}. {option}")
    pet_policy_choice = int(input()) - 1

    # Handling Pet Policy:
    if pet_policy_options[pet_policy_choice] == 'Yes':
        query_params['IF_PETS_ALLOWED'] = ('==', 'Allowed')
    elif pet_policy_options[pet_policy_choice] == 'No':
        query_params['IF_PETS_ALLOWED'] = ('==', 'Not Allowed')

    # Asking for Facilities (multiple choices allowed)
    print("\nWhich facilities would you like nearby? (Enter numbers separated by commas)")
    for idx, option in enumerate(facilities_options):
        print(f"{idx + 1}. {option}")
    facilities_choice = input().split(',')

    # Filter only for valid facility choices (skip "Not to matter")
    facilities = [facilities_options[int(facility.strip()) - 1] for facility in facilities_choice if facilities_options[int(facility.strip()) - 1] != 'Not to matter']

    # Asking for Crime Level
    while True:
        print("\nWhat's your crime level preference? (Enter number)")
        for idx, option in enumerate(crime_options):
            print(f"{idx + 1}. {option}")
        crime_choice = int(input()) - 1
        
        # Validate the input
        if 0 <= crime_choice < len(crime_options):
            break  # Input is valid, break out of the loop
        else:
            print("Invalid choice. Please enter a number between 1 and", len(crime_options))

    if crime_options[crime_choice] != 'Not to matter':
        query_params['Safety_level'] = ('==', crime_options[crime_choice])

    return query_params, facilities


# Main program
if __name__ == "__main__":
    print("Welcome to the Apartment Sorting Application!\n")
    
    # Collecting user preferences once
    query_params, facilities = collect_preferences()
    print(query_params)
