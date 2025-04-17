import requests
import csv
import os


def fetch_20_mps(url, mp_data, i):

    '''Returns a list of 20 MPs using parliament's API
    Params select current members and members of HoC

    Args:
        url (string): API to query for MP data
        mp_data (array): Array of MPs collected so far
        i (int): How far to skip through list (i=2 means start from 40th MP)

    Returns:
        mp_data (array): Array of MPs collected
        num (int): How many MPs were fetched in this function call
    '''

    params = {
        "IsCurrentMember": "true", 
        "House": "1", 
        "skip": (i*20) 
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    for mp in data['items']:
        # id = mp['value'].get(id) if id is needed
        name = mp['value'].get('nameDisplayAs')
        constituency = mp['value'].get('latestHouseMembership').get('membershipFrom')
        
        mp_data.append([name, constituency])

    num = len(data['items'])

    return mp_data, num


def fetch_mps(url):

    '''Parliament's API can only return 20 values at a time, so repeatedly calls fetch_20_mps

    Args:
        url (string): API to query

    Returns:
        mp_data (array): Array containing info about all the current MPs
    '''

    mp_data = []
    num = 20
    iterations = 0
    while num != 0:
        mp_data, num = fetch_20_mps(url, mp_data, iterations)
        iterations += 1

    return mp_data

def convert_to_csv(mp_data, final_csv_path):

    '''Take in an array and writes it to a csv

    Args:
        mp_data (array): Array of MP data
        final_csv_path: Where to save the csv
    '''

    fields = ['Name', 'Constituency']

    with open(final_csv_path, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(fields)
        csv_writer.writerows(mp_data)
        

if __name__ == "__main__":

    url = "https://members-api.parliament.uk/api/Members/Search"

    mp_data = fetch_mps(url)

    filename = "parliament.csv"

    csv_dir = os.path.abspath(".csvs")
    full_path = os.path.join(csv_dir, filename)

    convert_to_csv(mp_data, full_path)
