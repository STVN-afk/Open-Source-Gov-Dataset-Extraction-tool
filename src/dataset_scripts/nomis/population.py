import io
import time
import requests
import pandas as pd

from helper_scripts import helper

# Has most up to date data, to match website do date=latestMINUS2 (2021)
def Population_Conversion():

    '''DESCRIPTION:
        Uses an API call to retrieve the desired dataset. Renames some of the columns to a desired name,
        then saves to csv
    '''

    formatted_date = helper.getDate()
    url = "https://www.nomisweb.co.uk/api/v01/dataset/NM_31_1.data.csv?geography=1778384897...1778384901,1778384941,1778384950,1778385143...1778385146,1778385159,1778384902...1778384905,1778384942,1778384943,1778384956,1778384957,1778385033...1778385044,1778385124...1778385138,1778384906...1778384910,1778384958,1778385139...1778385142,1778385154...1778385158,1778384911...1778384914,1778384954,1778384955,1778384965...1778384972,1778385045...1778385058,1778385066...1778385072,1778384915...1778384917,1778384944,1778385078...1778385085,1778385100...1778385104,1778385112...1778385117,1778385147...1778385153,1778384925...1778384928,1778384948,1778384949,1778384960...1778384964,1778384986...1778384997,1778385015...1778385020,1778385059...1778385065,1778385086...1778385088,1778385118...1778385123,1778385160...1778385192,1778384929...1778384940,1778384953,1778384981...1778384985,1778385004...1778385014,1778385021...1778385032,1778385073...1778385077,1778385089...1778385099,1778385105...1778385111,1778384918...1778384924,1778384945...1778384947,1778384951,1778384952,1778384973...1778384980,1778384998...1778385003,1778384959,1778385193...1778385257&date=latestMINUS2&sex=7&age=0&measures=20100&select=geography_name,obs_value"
    response = requests.get(url)

    if response.status_code == 429:
        print("Rate limit exceeded, waiting")
        time.sleep(60)
        return Population_Conversion()
    elif response.status_code in [502, 504]:
        print("Skipping because of server issues")
        return None
    
    df = pd.read_csv(io.StringIO(response.text))

    df.rename(columns={'GEOGRAPHY_NAME':'local authority', 'OBS_VALUE':'numbers'}, inplace=True)

    output_path = helper.filePath(f"Population_{formatted_date}.csv", ".csvs") 
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    Population_Conversion()