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

# Loads API key
load_dotenv()
API_KEY = os.getenv("COMPANIES_HOUSE_API_KEY")

def process_rows(trust_data):
    '''For each trust, adds a row in the table containing their info,
        then uses fetch_parents to get info about any parent companies
        
    Args:
        trust_data (csv): csv data containing all the trusts and their companies house number
        
    Returns:
        companies_info (array): Every trust's parentage data
    '''
    
    companies_info = []
    for index, row in trust_data.iterrows():
        company_id = row['Companies house number']
        company_name = row['Group name']
        ukprn = row['UKPRN']

        companies_info.append({
            'Subsidiary ID': "",
            'Company ID': company_id,
            'Company Name': company_name,
            'UKPRN': ukprn,
            'Country': "England",
            'Degrees Removed': 0
        })

        companies_info = fetch_parents(companies_info, company_id, ukprn)

    return companies_info



def fetch_parents(companies_info, subsidiary_id, ukprn, degrees_removed=1):

    '''Recursively calls fetch_parent to get the full parentage for a trust
        Adds all this to the academy_info array
        Challenge: Some charities etc. listed as parent companies, don't have CH numbers
            so their CH number in the table is blank

    Args:
        companies_info (array): Trusts' parentage data
        subsidiary_id (string): Companies House ID of company
        ukprn (string): Identifier for school trusts
        degrees_removed (int): How far removed a company is from a trust

    Returns:
        companies_info (arrray): Trusts' parentage data
    '''

    parent = fetch_parent(subsidiary_id)
    if not parent:
        return companies_info

    parent_id = parent.get('identification', {}).get('registration_number')
    parent_name = parent.get('name')
    parent_country = parent.get('identification', {}).get('country_registered')

    companies_info.append({
        'Subsidiary ID': subsidiary_id,
        'Company ID': parent_id,
        'Company Name': parent_name,
        'UKPRN': ukprn,
        'Country': parent_country,
        'Degrees Removed': degrees_removed
    })

    # Check if it is a British company (if it isn't it doesn't have a CH number, can't trace further)
    if parent_id and any(loc in parent_country.lower() for loc in ["england", "wales", "united kingdom"]):
        fetch_parents(companies_info, parent_id, ukprn, degrees_removed + 1)
    
    return companies_info


# Stops function exceeding API rate limit
@sleep_and_retry
@limits(calls=REQUESTS, period = PERIOD)
def fetch_parent(company_number):

    # What to do with server issues

    '''For the company provided, return their parent company if they have one
        Checks for rate limits, lack of authorisation and server-side errors
    
    Args: 
        company_id (str): The Companies House ID of the company

    Returns:
        item (dict): The information about the company's parent
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
