import requests
import pandas as pd
from io import StringIO

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

if __name__ == "__main__":
    Employment_Conversion()