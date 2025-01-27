# File: apartment_crawler.py
# Group members: rivenl, leylal, chengkac, bangminp

# This script scrapes apartment data from Zillow and processes it to extract relevant details
# such as apartment name, rent, pet policies, and nearby schools. The data is either scraped
# fresh or loaded from a predownloaded file based on user input. The resulting data is saved
# as a CSV file in the raw folder for further processing.

# This file imports configuration settings from the `config.py` module and uses predefined
# functions to extract apartment details and handle pet policy, school information, and
# appliances. The scraped or predownloaded data is returned as a DataFrame for further processing.

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from config import *  

# Define headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.google.com',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document'
}

def scrape_apartment_data(pages_to_scrape=20):
    """Scrapes apartment data from Zillow or loads predownloaded data based on user choice."""
    
    # Ask user whether they want to use predownloaded data or scrape fresh data
    predownload_or_not = input(
        "It may take around 15 minutes to scrape fresh apartment data.\n"
        "Do you want to use predownloaded apartment data instead? (y/n): "
    ).strip().lower()

    if predownload_or_not == "y" and os.path.exists(PREDOWNLOAD_APARTMENT_DATA_PATH):
        print("Loading predownloaded apartment data...")
        apartment_df = pd.read_csv(PREDOWNLOAD_APARTMENT_DATA_PATH)
        return apartment_df
    else:
        print("Scraping fresh apartment data from Zillow...")

        # Initialize an empty list to store apartment data
        apartment_data = []

    def extract_text(soup, selectors, default='N/A'):
        """Helper function to extract text using multiple selectors."""
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.text.strip():
                return element.text.strip()
        return default

    def extract_pet_policy(soup, data_test_id):
        """Helper function to extract pet policy from the specified div."""
        try:
            policy_div = soup.find('div', {'data-test-id': data_test_id})
            if policy_div:
                li_items = policy_div.find_all('li', class_='ListItem-c11n-8-101-4__sc-13rwu5a-0 fxuoli')
                policies = [li.find('span', class_='Text-c11n-8-101-4__sc-aiai24-0 gtFYdd').text.strip() for li in li_items if li.find('span', class_='Text-c11n-8-101-4__sc-aiai24-0 gtFYdd')]
                return ', '.join(policies) if policies else 'N/A'
            return 'N/A'
        except Exception:
            return 'N/A'

    def extract_pets_allowed(soup):
        """Helper function to extract pets allowed policy under 'Management' heading."""
        try:
            management_section = soup.find('h6', text='Management')
            if management_section:
                parent_div = management_section.find_parent('div', {'data-testid': 'fact-category'})
                if parent_div:
                    li_items = parent_div.find_all('li', class_='ListItem-c11n-8-100-1__sc-13rwu5a-0 dWrjmG')
                    for li in li_items:
                        pets_allowed = li.find('span', class_='Text-c11n-8-100-1__sc-aiai24-0 jbRdkh')
                        if pets_allowed and 'Pets allowed' in pets_allowed.text:
                            return 'Yes' if 'Yes' in pets_allowed.text else 'No'
            return 'N/A'
        except Exception:
            return 'N/A'

    def extract_appliances(soup):
        """Extract appliance information from different possible structures and return as a comma-separated string."""
        appliances_list = []
        try:
            appliances_div = soup.find('div', {'data-test-id': 'building-amenity-appliances'})
            if appliances_div:
                li_items = appliances_div.find_all('li', class_='ListItem-c11n-8-101-4__sc-13rwu5a-0 fxuoli')
                for li in li_items:
                    appliance = li.find('span', class_='Text-c11n-8-101-4__sc-aiai24-0 gtFYdd')
                    if appliance and appliance.text.strip():
                        appliances_list.append(appliance.text.strip())

            appliances_category_div = soup.find('div', class_='fact-category')
            if appliances_category_div:
                ul_items = appliances_category_div.find_all('ul', class_='List-c11n-8-100-1__sc-1smrmqp-0 styles__StyledFactCategoryFactsList-fshdp-8-100-2__sc-1i5yjpk-1 nZbpv bREKeA')
                for ul in ul_items:
                    li_items = ul.find_all('li', class_='ListItem-c11n-8-100-1__sc-13rwu5a-0 dWrjmG')
                    for li in li_items:
                        appliance = li.find('span', class_='Text-c11n-8-100-1__sc-aiai24-0 jbRdkh')
                        if appliance and appliance.text.strip():
                            appliances_list.append(appliance.text.strip())

            return ', '.join(appliances_list) if appliances_list else 'N/A'
        except Exception:
            return 'N/A'

    def extract_schools_structure_1(soup):
        """Extract school information from the first structure."""
        school_info = {}
        school_list = soup.find('ul', class_='List-c11n-8-101-4__sc-1smrmqp-0 qjARs')
        if school_list:
            school_items = school_list.find_all('li', class_='ListItem-c11n-8-101-4__sc-13rwu5a-0 sc-eVZGIO knfXza jZa-dWq')
            for i in range(min(3, len(school_items))):  # Limit to 3 schools
                school_item = school_items[i]
                school_name_tag = school_item.find('a', class_='StyledTextButton-c11n-8-101-4__sc-1nwmfqo-0 fvRKOm notranslate')
                school_name = school_name_tag.text.strip() if school_name_tag else 'N/A'
                grades_div_parent = school_item.find('div', class_='Spacer-c11n-8-101-4__sc-17suqs2-0 dVGeMt')
                grades_span = grades_div_parent.find('span', class_='Text-c11n-8-101-4__sc-aiai24-0 jyAa-dJ') if grades_div_parent else None
                grades = grades_span.text.strip() if grades_span else 'N/A'
                rank_span = school_item.find('span', class_='Text-c11n-8-101-4__sc-aiai24-0 kcINhd')
                rank = rank_span.text.strip() if rank_span else 'N/A'
                school_info[f'school_name_{i+1}'] = school_name
                school_info[f'Grades_{i+1}'] = grades
                school_info[f'Rank_{i+1}'] = rank
        return school_info

    def extract_schools_structure_2(soup):
        """Extract school information from the second structure (GreatSchools rating)."""
        school_info = {}
        schools_section = soup.find('h5', text='GreatSchools rating')
        if schools_section:
            parent_div = schools_section.find_next('div', class_='Spacer-c11n-8-100-1__sc-17suqs2-0 sc-jRWcDx dQqFYn')
            if parent_div:
                school_items = parent_div.find_all('li', class_='ListItem-c11n-8-100-1__sc-13rwu5a-0 sc-fiDBSu sjBJu ekjldB')
                for i in range(min(3, len(school_items))):  # Limit to 3 schools
                    school_item = school_items[i]
                    school_name_tag = school_item.find('a', class_='StyledTextButton-c11n-8-100-1__sc-1nwmfqo-0 hcHpXi notranslate')
                    school_name = school_name_tag.text.strip() if school_name_tag else 'N/A'
                    grades_tag = school_item.find('span', class_='Text-c11n-8-100-1__sc-aiai24-0 kbVOjR')
                    grades = grades_tag.text.strip() if grades_tag else 'N/A'
                    rating_tag = school_item.find('span', class_='Text-c11n-8-100-1__sc-aiai24-0 bENqXR')
                    rating = rating_tag.text.strip() if rating_tag else 'N/A'
                    school_info[f'school_name_{i+1}'] = school_name
                    school_info[f'Grades_{i+1}'] = grades
                    school_info[f'Rating_{i+1}'] = rating
        return school_info

    for page_number in range(1, pages_to_scrape + 1):  # Adjust the range to the number of pages you want to scrape
        if page_number == 1:
            url = 'https://www.zillow.com/new-york-ny/apartments/1-bedrooms/'
        else:
            url = f'https://www.zillow.com/new-york-ny/apartments/1-bedrooms/{page_number}_p/'

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            ul = soup.find('ul', class_='List-c11n-8-105-0__sc-1smrmqp-0 StyledSearchListWrapper-srp-8-105-0__sc-1ieen0c-0 fNTnXQ dtRiBi photo-cards photo-cards_extra-attribution')

            if ul:
                li_items = ul.find_all('li', class_='ListItem-c11n-8-105-0__sc-13rwu5a-0 StyledListCardWrapper-srp-8-105-0__sc-wtsrtn-0 gpgmwS cXzrsE')

                for li in li_items:
                    link_tag = li.find('a', href=True)
                    if link_tag:
                        apartment_url = link_tag['href']
                        if not apartment_url.startswith('http'):
                            apartment_url = "https://www.zillow.com" + apartment_url

                        try:
                            apartment_response = requests.get(apartment_url, headers=headers)
                            apartment_response.raise_for_status()

                            apartment_soup = BeautifulSoup(apartment_response.text, 'html.parser')

                            apartment_name = extract_text(apartment_soup, ['h1[data-test-id="bdp-building-title"]', 'h1.Text-c11n-8-100-1__sc-aiai24-0.jbRdkh'])
                            apartment_address = extract_text(apartment_soup, ['h2[data-test-id="bdp-building-address"]', 'h1.Text-c11n-8-100-1__sc-aiai24-0.jbRdkh'])
                            apartment_rent = extract_text(apartment_soup, ['span[data-test-id="base-rent"]', 'button.TriggerText-c11n-8-100-1__sc-d96jze-0.BpPaS.TooltipPopper-c11n-8-100-1__sc-1v2hxhd-0.dYtaCG'])
                            features = extract_text(apartment_soup, [
                                'div.AtAGlanceFactsHollywood__StyledContainer-sc-34d077-0.jevfwQ',  # Structure 1
                                'div.hdp__sc-1nwbd1e-0.dcGsBQ'  # Structure 2
                            ])
                            appliances = extract_appliances(apartment_soup)

                            dog_policy = extract_pet_policy(apartment_soup, 'building-null-dogs-policy')
                            cat_policy = extract_pet_policy(apartment_soup, 'building-null-cats-policy')
                            large_dog_policy = extract_pet_policy(apartment_soup, 'building-large-dogs-policy')
                            small_dog_policy = extract_pet_policy(apartment_soup, 'building-small-dogs-policy')
                            pets_allowed = extract_pets_allowed(apartment_soup)

                            school_info_1 = extract_schools_structure_1(apartment_soup)
                            school_info_2 = extract_schools_structure_2(apartment_soup)
                            school_info_combined = {**school_info_1, **school_info_2}

                            apartment_data.append({
                                'Apartment Name': apartment_name,
                                'Address': apartment_address,
                                'Rent': apartment_rent,
                                'Features': features,
                                'Appliances': appliances,
                                'Dogs Policy': dog_policy,
                                'Cats Policy': cat_policy,
                                'Large Dogs Policy': large_dog_policy,
                                'Small Dogs Policy': small_dog_policy,
                                'Pets Allowed': pets_allowed,
                                **school_info_combined
                            })

                            time.sleep(random.uniform(2, 5))

                        except requests.exceptions.RequestException as e:
                            print(f"Failed to retrieve apartment data from {apartment_url}: {e}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve page {page_number}: {e}")

    # Store the apartment data in a DataFrame
    df = pd.DataFrame(apartment_data)
    
    return df

if __name__ == '__main__':
  # Call the function to scrape and save the data
  apartment_df = scrape_apartment_data()
  print(apartment_df)
