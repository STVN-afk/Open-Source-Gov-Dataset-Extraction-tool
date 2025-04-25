import io
import time
import requests
import pandas as pd

from helper_scripts import helper

def National_Averages_Conversion():

    '''DESCRIPTION:
        Uses an API call to retrieve the desired dataset. Renames one of the columns to a desired column 
        name, then saves to csv
    '''

    formatted_date = helper.getDate()
    url = "https://www.nomisweb.co.uk/api/v01/dataset/NM_17_5.data.csv?geography=2092957699&date=latest&variable=18,45,83&measures=20599,21001,21002,21003&select=variable_name,measures_name,obs_value&rows=variable_name&cols=measures_name"
    response = requests.get(url)

    if response.status_code == 429:
        print("Rate limit exceeded, waiting")
        time.sleep(60)
        return National_Averages_Conversion()
    elif response.status_code in [502, 504]:
        print("Skipping because of server issues")
        return None
    

    df = pd.read_csv(io.StringIO(response.text))
    df = df.rename(columns={"Variable":"percent"})

    output_path = helper.filePath(f"NationalAverages_{formatted_date}.csv", ".csvs") 
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    National_Averages_Conversion()