import io
import time
import requests
import pandas as pd

from helper_scripts import helper

def Population_Estimate_Conversion(gender_code):

    '''DESCRIPTION:
        Uses an API call to retrieve the desired dataset. Pivots the ages to become columns instead of rows,
        and depending on the gender_code inputted, gets data for male or female, adds a column stating the 
        gender and saves to a file that specifies the gender
    '''

    formatted_date = helper.getDate()
    url = f"https://www.nomisweb.co.uk/api/v01/dataset/NM_2002_1.data.csv?geography=1853882369...1853882372,1853882374...1853882377,1853882380...1853882382,2092957697...2092957703,1774190593...1774190597,1774190637,1774190646,1774190675...1774190678,1774190691,1774190598...1774190601,1774190638,1774190639,1774190652,1774190653,1774190656...1774190670,1774190734,1774190602...1774190606,1774190654,1774190671...1774190674,1774190686...1774190690,1774190607...1774190610,1774190650,1774190651,1774190726,1774190735,1774190736,1774190738,1774190611...1774190613,1774190640,1774190679...1774190685,1774190740,1774190743,1774190745,1774190621...1774190624,1774190644,1774190645,1774190725,1774190729,1774190732,1774190737,1774190741,1774190692...1774190724,1774190625...1774190636,1774190649,1774190728,1774190731,1774190733,1774190739,1774190742,1774190744,1774190614...1774190620,1774190641...1774190643,1774190647,1774190648,1774190655,1774190727,1774190730,1774190746...1774190810,1778384897...1778384901,1778384941,1778384950,1778385143...1778385146,1778385159,1778384902...1778384905,1778384942,1778384943,1778384956,1778384957,1778385033...1778385044,1778385124...1778385138,1778384906...1778384910,1778384958,1778385139...1778385142,1778385154...1778385158,1778384911...1778384914,1778384954,1778384955,1778384965...1778384972,1778385045...1778385058,1778385066...1778385072,1778384915...1778384917,1778384944,1778385078...1778385085,1778385100...1778385104,1778385112...1778385117,1778385147...1778385153,1778384925...1778384928,1778384948,1778384949,1778384960...1778384964,1778384986...1778384997,1778385015...1778385020,1778385059...1778385065,1778385086...1778385088,1778385118...1778385123,1778385160...1778385192,1778384929...1778384940,1778384953,1778384981...1778384985,1778385004...1778385014,1778385021...1778385032,1778385073...1778385077,1778385089...1778385099,1778385105...1778385111,1778384918...1778384924,1778384945...1778384947,1778384951,1778384952,1778384973...1778384980,1778384998...1778385003,1778384959,1778385193...1778385257,1937768449...1937768456,2013265921...2013265932&date=latest&gender={gender_code}&c_age=101...191&measures=20100&select=date_name,geography_name,geography_type,c_age_name,obs_value"
    response = requests.get(url)

    if response.status_code == 429:
        print("Rate limit exceeded, waiting")
        time.sleep(60)
        return Population_Estimate_Conversion()
    elif response.status_code in [502, 504]:
        print("Skipping because of server issues")
        return None


    df = pd.read_csv(io.StringIO(response.text), dtype={'OBS_VALUE': str})

    pivot_df = df.pivot_table(
    index=['DATE_NAME','GEOGRAPHY_TYPE','GEOGRAPHY_NAME'],
    columns='C_AGE_NAME',
    values='OBS_VALUE',
    aggfunc='first' 
    ).reset_index()

    # Changes order of age columns (from Age 1, Age 10, Age 11 to ascending order)
    # Looks at age columns and sorts by the digits in them
    index_cols = ["DATE_NAME","GEOGRAPHY_TYPE","GEOGRAPHY_NAME"]
    age_cols = [col for col in pivot_df.columns if col not in index_cols]
    age_cols_sorted = sorted(age_cols, key=lambda x: int(''.join(filter(str.isdigit, x)) or -1))
    pivot_df = pivot_df[index_cols + age_cols_sorted]


    if gender_code == 1:
        pivot_df.insert(1, 'Gender', 'M') 
    if gender_code == 2:
        pivot_df.insert(1, 'Gender', 'F')


    output_path = helper.filePath(f"PopulationEstimates_{'Male' if gender_code == 1 else 'Female'}_{formatted_date}.csv", ".csvs") 
    pivot_df.to_csv(output_path, index=False)


def Population_Estimates():

    '''DESCRIPTION:
        Calls Population_Estimate_Conversion() twice to create two files, one with data about men and the 
        other with data about women
    '''
    Population_Estimate_Conversion(1) # Male
    Population_Estimate_Conversion(2) # Female


if __name__ == "__main__":
    Population_Estimates()