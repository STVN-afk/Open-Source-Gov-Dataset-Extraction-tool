import io
import time
import requests
import pandas as pd
import os

from helper_scripts import helper

def Unemployment_Conversion():

    ''' 
        DESCRIPTION: 
            Uses an API call to retrieve the wanted dataset. Values are from 2 separate tables therefore 
            to create the final csv file, the tables needed to be formatted and then merged together.

        HOW TO GENERATE LINK MANUALLY:
            Dataset: model-based estimates of unemployment

            To get Columns -- 
            Geography: local authorities: district / unitary (as of April 2023)
            Date: Dec 2024
            Variable: Unemployment Count, Unemployment Rate
    '''
    
    formatted_date = helper.getDate()
    url = "https://www.nomisweb.co.uk/api/v01/dataset/NM_127_1.data.csv?geography=1778384897...1778384901,1778384941,1778384950,1778385143...1778385146,1778385159,1778384902...1778384905,1778384942,1778384943,1778384956,1778384957,1778385033...1778385044,1778385124...1778385138,1778384906...1778384910,1778384958,1778385139...1778385142,1778385154...1778385158,1778384911...1778384914,1778384954,1778384955,1778384965...1778384972,1778385045...1778385058,1778385066...1778385072,1778384915...1778384917,1778384944,1778385078...1778385085,1778385100...1778385104,1778385112...1778385117,1778385147...1778385153,1778384925...1778384928,1778384948,1778384949,1778384960...1778384964,1778384986...1778384997,1778385015...1778385020,1778385059...1778385065,1778385086...1778385088,1778385118...1778385123,1778385160...1778385192,1778384929...1778384940,1778384953,1778384981...1778384985,1778385004...1778385014,1778385021...1778385032,1778385073...1778385077,1778385089...1778385099,1778385105...1778385111,1778384918...1778384924,1778384945...1778384947,1778384951,1778384952,1778384973...1778384980,1778384998...1778385003,1778384959,1778385193...1778385246&date=latest&item=1,2&measures=20100,20701"
    
    response = requests.get(url)

    df = pd.read_csv(io.StringIO(response.text))
    
    # Merges 4 geography places into 2 (one for each variable)
    reshaped_df = df.pivot_table(
            index=["GEOGRAPHY_NAME", "ITEM_NAME"],
            columns="MEASURES_NAME",
            values="OBS_VALUE"
        ).reset_index()
    
    # Flattens into 1 so that both variables are in 1 record
    flat_df = reshaped_df.pivot_table(
        index=["GEOGRAPHY_NAME"],
        columns="ITEM_NAME",
        values=["Value"]
        ).reset_index()
    
    # Cleansing 
    flat_df = flat_df.iloc[0:].reset_index(drop=True)
    flat_df.columns = ["Local Authority", "numbers", "%"]
    flat_df["numbers"] = flat_df["numbers"].astype(int)

    # Saves at path 
    output_path = helper.filePath(f"Unemployed_{formatted_date}.csv", ".csvs") 
    flat_df.to_csv(output_path,index=False)


if __name__ == "__main__":
    Unemployment_Conversion()