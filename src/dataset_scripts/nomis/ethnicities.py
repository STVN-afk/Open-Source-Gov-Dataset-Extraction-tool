import io
import time
import requests
import pandas as pd

from helper_scripts import helper

def Ethnicities_Conversion():

    '''DESCRIPTION:
        Uses an API call to retrieve the desired dataset. Some values need to be pivoted to become columns,
        hence the line that pivots them
 
    '''

    formatted_date = helper.getDate()

    url = "https://www.nomisweb.co.uk/api/v01/dataset/NM_608_1.data.csv?date=latest&geography=1946157057...1946157404&rural_urban=0&cell=0,100,200,300,400,500&measures=20301&select=geography_name,obs_value,cell_name"
    response = requests.get(url)

    if response.status_code == 429:
        print("Rate limit exceeded, waiting")
        time.sleep(60)
        return Ethnicities_Conversion()
    elif response.status_code in [502, 504]:
        print("Skipping because of server issues")
        return None
    
    df = pd.read_csv(io.StringIO(response.text))

    pivot_df = df.pivot(index='GEOGRAPHY_NAME', columns='CELL_NAME', values='OBS_VALUE').reset_index()

    output_path = helper.filePath(f"EthnicGroup_{formatted_date}.csv", ".csvs") 
    pivot_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    Ethnicities_Conversion()