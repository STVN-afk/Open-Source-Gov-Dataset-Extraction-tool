import requests
from requests.auth import HTTPBasicAuth
from helper_scripts import helper
import pandas as pd
import os
from dotenv import load_dotenv
from helper_scripts import helper
import time
import sys
from ratelimit import limits, sleep_and_retry

# API allows 600 requests in 5 minutes
REQUESTS = 500
PERIOD = 300

# Load API key environment variable
load_dotenv()
API_KEY = os.getenv("COMPANIES_HOUSE_API_KEY")



def process_rows(trust_data):

    '''For each trust in the data, calls get_officers
    
    Args: 
        trust_data (csv): The file containing the trusts
        
    Returns:
        officers_info (array): Collection of info around officers'''

    officers_info = []
    for index, row in trust_data.iterrows():
        company_id = row['Companies house number']
        ukprn = row['UKPRN']

        for officer in get_officers(company_id):
            officers_info.append({
                'Companies House Number': company_id,
                'UKPRN': ukprn,
                'Name': officer['name'],
                'Officer Role': officer['officer_role'],
                'Appointed On': officer['appointed_on'],
                'Resigned On': officer.get('resigned_on', 'N/A')
            })

    return officers_info
        
@sleep_and_retry
@limits(calls=REQUESTS, period = PERIOD)
def get_officers(company_id):

    '''For the company provided, return their past and present officers,
        Checks for rate limits, lack of authorisation and server-side errors
    
    Args: 
        company_id (str): The Companies House ID of the company

    Returns:
        data['items'] (dict): The JSON response from querying the API
    '''
    
    url = f'https://api.company-information.service.gov.uk/company/{company_id}/officers'
    response = requests.get(url, auth=HTTPBasicAuth(API_KEY, ''))


    if response.status_code == 429:
        print("Rate limit exceeded, waiting")
        time.sleep(60)
        return get_officers(company_id)
    elif response.status_code == 401:
        print("Unauthorized: Can't gain access")
        sys.exit()
    elif response.status_code in [502, 504]:
        print("Skipping because of server issues")
        return None
    

    data = response.json()
    return data['items']


def save_data(data): 

    '''Saves the supplied data into a csv file

    Args:
        data (array): The data about company officers
    '''

    df = pd.DataFrame(data)

    output_path = helper.filePath("trust_officers.csv", ".csvs") 
    df.to_csv(output_path, index=False)






if __name__ == "__main__":
    file_path = helper.filePath("GroupExtract.csv", "input_data")
    input = pd.read_csv(file_path, encoding='ISO-8859-1', dtype={'Companies house number': str})
    input = input.head(10)

    officers = process_rows(input)
    save_data(officers)



