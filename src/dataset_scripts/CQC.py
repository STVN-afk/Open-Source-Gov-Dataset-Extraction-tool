import pandas as pd 
import os, datetime, ezodf
import requests

''' Uses ezodf because the load times for pandas average around 300s or 5 minutes whilst ezodf reads the file within 30 seconds '''

# Finds path to download 
download_dir = os.path.abspath("downloads")
csv_dir = os.path.abspath(".csvs")



'''
def createDriver():

    # Preferences
    driver_options = Options()
    driver_options.set_preference("browser.download.folderList", 2)  # custom location
    driver_options.set_preference("browser.download.dir", download_dir)
    driver_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")  # adjust MIME type
    driver_options.set_preference("pdfjs.disabled", True)  # disable built-in viewer

    # Creates Driver and requests the url page 
    driver = webdriver.Firefox(options=driver_options)
    return driver 

'''

def conversion_from_ods_to_csv(filename):
    print("Starting Conversion")
    pd.read_excel(filename, engine="odf")
    print("read file")

'''
def downloadFiles(driver):

    care_csv = driver.find_element(By.PARTIAL_LINK_TEXT, "csv")
    file_name = care_csv.get_attribute("href").split("/")[-1]
    
    if os.path.exists(os.path.join(download_dir,file_name)):
        print(file_name + " Already Exists")
    else:
        print("downloaded csv file " + file_name)
        driver.execute_script("arguments[0].click();", care_csv)
        time.sleep(2)
    
    btnlinks = driver.find_elements(By.XPATH, "//a[contains(@href, '.ods')]")
 
    for x in btnlinks:
        file_url = x.get_attribute("href")
        file_name = file_url.split("/")[-1]
        decoded_file_name = urllib.parse.unquote(file_name)
       
        if os.path.exists(os.path.join(download_dir,decoded_file_name)):
            print(file_name + " Already Exists")
        else:
            print("downloading ods file " + decoded_file_name)
            driver.execute_script("arguments[0].click();", x)
            time.sleep(2) 
    
    time.sleep(2)
    driver.close()
           
'''
def downloadFiles(urls):
    for url in urls:
        local_filename = os.path.basename(url)

        try:
            if ".csv" in url:
                print("Reading in csv")
                read_file = pd.read_csv(url)
                read_file.to_csv(str(local_filename).replace(".ods",".csv"))
                print("downloaded")
            else:
                print("Reads Ods file (1st sheet)")
                response = requests.get(url)
                print(response.raise_for_status)

            

                with open(local_filename, 'wb') as f:
                    f.write(response.content)

                df = ezodf.opendoc(local_filename)

                final_list = []
    
                # Remove comments if you want to use pandas 
                '''
                df = pd.ExcelFile(local_filename)

                sheet_names = [sheet for sheet in df.sheet_names if sheet != "README"]

                for sheet in sheet_names:
                    sheet_file = pd.read_excel(local_filename,sheet_name=sheet)

                    sheet_file["Sheetname"] = sheet
                    final_list.append(sheet_file)

                if final_list:
                    final_df = pd.concat(final_list, ignore_index=True)
                
                    final_df.to_csv(str(local_filename).replace(".ods",".csv"), index=False)
                    print("Merged CSV created successfully!")
                else:
                    print("No valid sheets found or all sheets were skipped.")

                
                '''
                
          

                #ezodf method
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

                            # Create a separator row DataFrame.
                            # This row will repeat across each column.
                            separator_row = pd.DataFrame([[f"----- {sheet.name} -----"] * len(df.columns)],
                                columns=df.columns)

                            # Creates a header
                            header_row = pd.DataFrame([df.columns.tolist()],
                            columns=df.columns)
                            
                            # Optionally add a blank row for additional visual separation.
                            blank_row = pd.DataFrame([[""] * len(df.columns)], columns=df.columns)

                            sheet_output = pd.concat([separator_row, blank_row, header_row, df, blank_row],ignore_index=True)

                            final_list.append(sheet_output)

                    # Concatenate all pieces into a single DataFrame.
                    if final_list:
                        final_df = pd.concat(final_list, ignore_index=True)
                        
                        # Save the combined DataFrame to a CSV file.
                        final_df.to_csv(str(local_filename).replace(".ods",".csv"),header=False, index = False)
                        print("Combined CSV created successfully!")
                    else:
                        print("No data was found in the sheets (or all sheets were skipped).")
                
            

                os.remove(local_filename)

                



                # Multiple tables in sheets separated by headers


        except Exception as e:
            print(e)
            print("Outdated, won't be downloaded")


    
            
if __name__ == "__main__":     
    ct = datetime.datetime.now()
    formatted_ct = ct.strftime("%Y-%m/%d_%B_%Y")
    deactivated_ct = formatted_ct.replace("_","%20")

    urls = ["https://www.cqc.org.uk/sites/default/files/" +formatted_ct+ "_CQC_directory.csv"
            ,"https://www.cqc.org.uk/sites/default/files/"+formatted_ct+ "_HSCA_Active_Locations.ods"
            ,"https://www.cqc.org.uk/sites/default/files/" +formatted_ct+ "_Latest_ratings.ods"
            ,"https://www.cqc.org.uk/sites/default/files/" +deactivated_ct+ "20Deactivated%20locations.ods"]
    
    test_urls = ["https://www.cqc.org.uk/sites/default/files/2025-04/02_April_2025_CQC_directory.csv"
                 ,"https://www.cqc.org.uk/sites/default/files/2025-04/01_April_2025_HSCA_Active_Locations.ods",
                 "https://www.cqc.org.uk/sites/default/files/2025-04/01_April_2025_Latest_ratings.ods",
                 "https://www.cqc.org.uk/sites/default/files/2025-04/01%20April%202025%20Deactivated%20locations.ods"]
    # Download Files 
    downloadFiles(test_urls)


