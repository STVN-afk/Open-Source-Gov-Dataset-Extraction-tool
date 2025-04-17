import pandas as pd 
import os, datetime
import requests
from helper_scripts import helper

# import ezodf

# Finds path to download 
download_dir = os.path.abspath("downloads")
csv_dir = os.path.abspath(".csvs")


def downloadFiles(urls):
    '''
    DESCRIPTION:
    Receives the url list and for each url, if it is a csv file, it is just downloaded if it is new
    however, if it returns an error message (404) that means that the file has not been updated and
    therefore we do not download it. If it is an ODS file, we use the requests package to retrieve the 
    url link. If the status code is 200 (request successful), we save the file locally and read it using 
    either pandas or ezodl. Afterwards, it is converted to a csv file for each sheet in the ods file and the 
    ods file is removed locally.

    PANDAS:
    Reads the entire ods file using the ExcelFile function and then filters out the README document in the
    excel file. Afterwards it parses the remaining sheets from the excel file and converts them into csv files.

    PANDAS ISSUE:
    Takes a long time to read and convert each sheet into csv files (average around 20 minutes for Active_location
    records, 50 minutes or 3000 seconds for Latest Ratings and 540 seconds or 9 minutes for Deactivated Locations.)

    EZODF:
    Creates the Dataframe manually by reading in the headers and the data and converting it to a dataframe.
    After, it is then converted using pandas into a csv file. This process takes around (5-10 minutes)

    EZODF ISSUE:
    Only issue is the integration of the package since the system is vulnerable to modifications.

    PARAMETERS:
    urls (list of str): List of url links to the respective ods files on the site with the current date.

    POTENTIAL ISSUES:
    Care home beds in the tables is set as a fault by default in the Bronze (raw) stage

    EXCEPTIONS:
    404: Not found therefore there is no link for the current date.
    200: Request Successful therefore there is a link for the current date.
    '''

    for url in urls:
        local_filename = os.path.basename(url)

        try:
            if ".csv" in url:
                print("Reading in csv")
                read_file = pd.read_csv(url)
                read_file.to_csv(str(local_filename).replace(".ods",".csv"))
                print(f"downloaded {local_filename}")
            else:
                response = requests.get(url)
                
                if response.status_code == 200:
                    with open(local_filename, 'wb') as f:
                        f.write(response.content)
                        print(f"downloaded {local_filename}")
        
                    df = pd.ExcelFile(local_filename)

                    sheet_names = [sheet for sheet in df.sheet_names if sheet != "README"]
                    print("got sheet names")

                    for sheet in sheet_names:
                        print(f"reading in {sheet} file ")
                        sheet_df = df.parse(sheet_name=sheet)
                        print("Completed Reading of File")

                        sheet_name = str(local_filename).replace(".ods", "_")
                        output_path = helper.filePath(f"{sheet_name}{sheet}.csv",".csvs")
                        sheet_df.to_csv(output_path,index=False)
                        print(f"Conversion of {sheet} is complete")
                                    
                    '''
                    #ezodf method

                    #df = ezodf.opendoc(local_filename)

                    for sheet in df.sheets:
                        if sheet.name == "README":
                            continue 
                        else:
                            data = []
                            for row in sheet.rows():
                                # For each row, get the value in each cell.
                                data.append([cell.value for cell in row])
                            
                            if data:
                                # We assume the first row is the header 
                                header = data[0]
                                # Data
                                table_data = data[1:]
                                

                                df = pd.DataFrame(table_data, columns=header)

                                columns_with_date = [col for col in df.columns if col is not None and "date" in col.lower()]
                            

                                # Changes format for dates to not include time in the date.
                                for column in columns_with_date:
                                    df[column] = pd.to_datetime(df[column], errors='coerce').dt.date

                                df.to_csv((str(local_filename).replace(".ods", "_") + sheet.name + ".csv"))
                                print("downloaded " + sheet.name)

                                '''
                else:
                    raise Exception("No URL link with that name")
                
        except Exception as e:
            print(e)
            
def geturls():
    
    '''
    DESCRIPTION:
    Using the datetime package, we retrieve the current date and then format it into the same format 
    as the hyperlink which is the following (Year-Month/Day_Month_Year). After formatting the date,
    we can then replace the dates on the hyperlink and return it.

    RETURNS:
    urls (list of str): List of url links to the respective ods files on the site with the current date.
    '''

    ct = datetime.datetime.now()
    formatted_ct = ct.strftime("%Y-%m/%d_%B_%Y")
    deactivated_ct = formatted_ct.replace("_","%20")

    urls = [f"https://www.cqc.org.uk/sites/default/files/{formatted_ct}_CQC_directory.csv",
            f"https://www.cqc.org.uk/sites/default/files/{formatted_ct}_HSCA_Active_Locations.ods",
            f"https://www.cqc.org.uk/sites/default/files/{formatted_ct}_Latest_ratings.ods",
            f"https://www.cqc.org.uk/sites/default/files/{deactivated_ct}20Deactivated%20locations.ods"
            ]
            
    return urls

if __name__ == "__main__":     
    
    urls = geturls()

    test_urls = ["https://www.cqc.org.uk/sites/default/files/2025-04/01_April_2025_HSCA_Active_Locations.ods"]

    '''
    Switch to urls when needed in the downloadFiles
    '''

    # Download Files 
    downloadFiles(test_urls)


