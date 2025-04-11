import requests
from requests.auth import HTTPBasicAuth
from helper_scripts import helper
import pandas as pd
import time
from ratelimit import limits, sleep_and_retry
import os
from dotenv import load_dotenv
import sys

# API allows 600 requests in 5 minutes
REQUESTS = 500
PERIOD = 300

# Load API key environment variable
load_dotenv()
API_KEY = os.getenv("COMPANIES_HOUSE_API_KEY")


# Removes schools that aren't academies
# Selects first 100 rows for testing purposes
def filter_rows(file):
    input = pd.read_csv(file, encoding='ISO-8859-1')
    filtered_input = input[input['PropsName'].notna()]
    return filtered_input.head(100)

# For each academy, if its proprietor is in CH, mark it as matching
def process_rows(input):
    for index, row in input.iterrows():
        proprietor = row['PropsName']
        if fetch_company(proprietor.lower()):
            input.at[index, 'proprietor matches'] = True
    return input

# Looks for company in companies house, returns True if they match
@sleep_and_retry
@limits(calls=REQUESTS, period = PERIOD)
def fetch_company(proprietor):
    url = f'https://api.company-information.service.gov.uk/search/companies?q={proprietor}'

    response = requests.get(url, auth=HTTPBasicAuth(API_KEY, ''))

    # If rate limit exceeded then wait
    if response.status_code == 429:
        print("Rate limit exceeded, waiting")
        time.sleep(60)
        return fetch_company(proprietor)
    
    if response.status_code == 401:
        print("Unauthorized: Can't gain access")
        sys.exit()

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

    output = process_rows(filtered_input)
    output.to_csv('.csvs/proprietors.csv', index=False)

