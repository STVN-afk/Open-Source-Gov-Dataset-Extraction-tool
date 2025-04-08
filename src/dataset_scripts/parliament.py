import requests
import csv
import os


def fetch_20_mps(url, mp_data, i):

    params = {
        "IsCurrentMember": "true",  # Filter for current MPs
        "House": "1", # Only MPs not Lords
        "skip": (i*20) # Start 0,20,40 etc. people in
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    for mp in data['items']:

        name = mp['value'].get('nameDisplayAs')
        constituency = mp['value'].get('latestHouseMembership').get('membershipFrom')
        
        mp_data.append([name, constituency])

    num = len(data['items'])

    return mp_data, num

# API can only do 20 at a time
# Continues until no more MPs found
# With each iteration, skip forward 20
def fetch_mps(url):
    mp_data = []
    num = 20
    iterations = 0
    while num != 0:
        mp_data, num = fetch_20_mps(url, mp_data, iterations)
        iterations += 1

    return mp_data

def convert_to_csv(mp_data):
    fields = ['Name', 'Constituency']

    filename = "parliament.csv"

    csv_dir = os.path.abspath(".csvs")
    full_path = os.path.join(csv_dir, filename)

    with open(full_path, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(fields)
        csv_writer.writerows(mp_data)
        

if __name__ == "__main__":

    url = "https://members-api.parliament.uk/api/Members/Search"

    mp_data = fetch_mps(url)
    convert_to_csv(mp_data)
