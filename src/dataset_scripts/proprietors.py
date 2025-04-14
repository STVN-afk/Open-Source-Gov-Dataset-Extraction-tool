import requests
from requests.auth import HTTPBasicAuth
from helper_scripts import helper
import pandas as pd
import time
from ratelimit import limits, sleep_and_retry
import os
from dotenv import load_dotenv
import sys

# Link for schools database: 
# ea-edubase-api-prod.azurewebsites.net/edubase/downloads/public/edubasealldataYYYYMMDD.csv

# API allows 600 requests in 5 minutes
REQUESTS = 500
PERIOD = 300

# Load API key environment variable
load_dotenv()
API_KEY = os.getenv("COMPANIES_HOUSE_API_KEY")


def filter_rows(file):

    """Filters out schools that aren't academies, currently just first 100 for testing

    Args:
        file (string): The filepath to find the input

    Returns:
        filtered_input: The file with non-academies removed
    """

    input = pd.read_csv(file, encoding='ISO-8859-1')
    filtered_input = input[input['PropsName'].notna()]
    return filtered_input.head(100)

def process_rows(academies):

    """Calls fetch_company for each row, returns file with proprietor columns updated
        (if there's a matching company, and that company's CH number)

    Args:
        input (csv): The data about all the academies

    Returns:
        input (csv): The academies with updated columns about proprietors
    """

    for index, row in academies.iterrows():
        proprietor = row['PropsName']
        if fetch_company(proprietor.lower()):
            academies.at[index, 'proprietor matches'] = True
    return academies

# Looks for company in companies house, returns True if they match
@sleep_and_retry
@limits(calls=REQUESTS, period = PERIOD)
def fetch_company(proprietor):

    time.sleep(0.3)

    '''Uses the CH API to search for proprietor of school in CH
        If the name matches, returns the company number.
        Has checks for lacking authorisation, hitting rate limit and server issues
        
    Args:
        proprietor (string): The name of the company to be searched for

    Returns: 

    '''

    url = f'https://api.company-information.service.gov.uk/search/companies?q={proprietor}'

    response = requests.get(url, auth=HTTPBasicAuth(API_KEY, ''))

    print(response.status_code)

    if response.status_code == 429:
        print("Rate limit exceeded, waiting")
        time.sleep(60)
        return fetch_company(proprietor)
    
    elif response.status_code == 401:
        print("Unauthorized: Can't gain access")
        sys.exit()

    elif response.status_code in [502, 504]:
        print("Skipping because of server issues")
        return None

    # If company name finds a match in CH, return true
    data = response.json()
    if data.get('items', []):
        closest_match = data['items'][0]
        if closest_match['title'].lower().strip() == proprietor.strip():
            return True
        else: 
            return False


if __name__ == "__main__":

    input = helper.filePath("edubasealldata20250409.csv", "input_data")

    filtered_input = filter_rows(input)
    filtered_input['proprietor matches'] = False
    # filtered_input['proprietor number'] = ''

    output = process_rows(filtered_input)
    output.to_csv('.csvs/proprietors.csv', index=False)

