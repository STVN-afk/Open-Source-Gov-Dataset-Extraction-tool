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

load_dotenv()
API_KEY = os.getenv("COMPANIES_HOUSE_API_KEY")

def process_rows(trust_data):
    '''For each trust, adds a row in the table containing their info,
        then uses fetch_parents to get info about any parent companies
        
    Args:
        trust_data (csv): csv data containing all the trusts and their companies house number
        
    Returns:
        academy_info (array): Every trust's parentage data
    '''
    
    academy_info = []
    for index, row in trust_data.iterrows():
        company_id = row['Companies house number']
        company_name = row['Group name']
        ukprn = row['UKPRN']

        academy_info.append({
            'Subsidiary ID': "",
            'Company ID': company_id,
            'Company Name': company_name,
            'UKPRN': ukprn,
            'Country': "England",
            'Degrees Removed': 0
        })

        fetch_parents(academy_info, company_id, ukprn)

    return academy_info



def fetch_parents(academy_info, subsidiary_id, ukprn, degrees_removed=1):

    '''Recursively calls fetch_parent to get the full parentage for a trust
        Adds all this to the academy_info array
        Challenge: Some charities etc. listed as parent companies, don't have CH numbers
    '''

    parent = fetch_parent(subsidiary_id)
    if not parent:
        return academy_info

    parent_id = parent.get('identification', {}).get('registration_number')
    parent_name = parent.get('name')
    parent_country = parent.get('identification', {}).get('country_registered')

    academy_info.append({
        'Subsidiary ID': subsidiary_id,
        'Company ID': parent_id,
        'Company Name': parent_name,
        'UKPRN': ukprn,
        'Country': parent_country,
        'Degrees Removed': degrees_removed
    })

    if parent_id and any(loc in parent_country.lower() for loc in ["england", "wales", "united kingdom"]):
        fetch_parents(academy_info, parent_id, ukprn, degrees_removed + 1)
    
    return academy_info



@sleep_and_retry
@limits(calls=REQUESTS, period = PERIOD)
def fetch_parent(company_number):

    # What to do with server issues

    '''For the company provided, return their past and present officers,
        Checks for rate limits, lack of authorisation and server-side errors
    
    Args: 
        company_id (str): The Companies House ID of the company

    Returns:
        data['items'] (dict): The JSON response from querying the API
    '''
    
    url = f'https://api.company-information.service.gov.uk/company/{company_number}/persons-with-significant-control'
    response = requests.get(url, auth=HTTPBasicAuth(API_KEY, ''))

    if response.status_code == 429:
        print("Rate limit exceeded, waiting")
        time.sleep(60)
        return fetch_parent(company_number)
    elif response.status_code == 401:
        print("Unauthorized: Can't gain access")
        sys.exit()
    elif response.status_code in [502, 504]:
        print("Skipping because of server issues")
        return None
    

    data = response.json()
    for item in data['items']:
        if item.get('kind') == 'corporate-entity-person-with-significant-control':
            if item.get('ceased') == False:
                return item


def save_data(data): 

    '''Saves the supplied data into a csv file

    Args:
        data (array): The data about company officers
    '''

    df = pd.DataFrame(data)

    output_path = helper.filePath("parent_companies.csv", ".csvs") 
    df.to_csv(output_path, index=False)




if __name__ == "__main__":

    file_path = helper.filePath("GroupExtract.csv", "input_data")
    input = pd.read_csv(file_path, encoding='ISO-8859-1', dtype={
        'Companies house number': str,
        'UKPRN': str})
    input = input.head(200)

    parent_companies = process_rows(input)
    save_data(parent_companies)
