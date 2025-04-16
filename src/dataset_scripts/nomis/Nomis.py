import io
import time
import requests
import pandas as pd
from io import StringIO

from helper_scripts import helper

def Employment_Conversion():
    

    url = "https://www.nomisweb.co.uk/api/v01/dataset/NM_17_1.data.csv"

    params = {
        "date": "latest",               # Get latest available data
        "geography": "TYPE113",         # All local authorities in Great Britain
        "variable": "18",               # In employment
        "measures": "20100",            # Count (value)
        "gender": "0",                  # All people
        "c_age": "0",                   # All ages
        "select": "GEOGRAPHY_NAME,DATE,OBS_VALUE"
    }

    rq = requests.get(url, params=params)


def Ethnicities_Conversion():
    url = "https://www.nomisweb.co.uk/api/v01/dataset/NM_608_1.data.csv?date=latest&geography=1946157057...1946157404&rural_urban=0&cell=0,100,200,300,400,500&measures=20301&select=geography_name,obs_value,cell_name"
    response = requests.get(url)

    if response.status_code == 429:
        print("Rate limit exceeded, waiting")
        time.sleep(60)
        return Ethnicities_Conversion()
    elif response.status_code in [502, 504]:
        print("Skipping because of server issues")
        return None
    
    # Read CSV into DataFrame
    df = pd.read_csv(io.StringIO(response.text))

    pivot_df = df.pivot(index='GEOGRAPHY_NAME', columns='CELL_NAME', values='OBS_VALUE').reset_index()

    output_path = helper.filePath("ethnicities.csv", ".csvs") 
    pivot_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    Employment_Conversion()