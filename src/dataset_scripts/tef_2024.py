import os

# Removed as Helper script has function to create driver making it redundant for below
# Remove comments if the creation of the driver is wanted on the script itself

#from selenium import webdriver
#from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.by import By
import pandas as pd 
import glob, time
import xlwings as xw
from helper_scripts import helper

def conversion_to_csv(filename):

    '''
        Checks if the file file can be read using the pd module, if there is an issue, that means 
        the excel file cannot be read using openpyxl (pd default engine).

        The xlwings module (needs to be downloaded) is used to open the file using excel in the case 
        it cannot be read by openpyxl and resaving the file using excel's default format which can then 
        be read in by the script.

        Currently the only workaround is using the xlwings module for this specific excel workbook

        After it reads in the excel file using pandas creates a path to the .csvs folder and saves it 
        there, then it deletes the excel file.
    '''

    while True:
        # Tries to read Excel file 
        try:
            file = pd.read_excel(filename, engine= "openpyxl")
        except Exception as e:
            path2 = filename 
            print("Failed to open workbook; error: ")
            print(e)
            # Opens path using excel app  
            wingsbook = xw.Book(path2)
            # gets active app, instance of excel
            wingsapp = xw.apps.active
            # Saves book using excel's logic 
            wingsbook.save(path2)
            wingsapp.quit()

            # Assigns new excel file as filename
            filename = path2
        else:
            break

    file = pd.read_excel(filename, engine= "openpyxl")
    csv_filename = os.path.splitext(os.path.basename(filename))[0] + ".csv"
    csv_path = os.path.join(os.path.abspath(".csvs"), csv_filename)
    file.to_csv(csv_path, index=False, quotechar="'")
    os.remove(filename)

'''
If 

def createDriver(link):
    # Preferences
    driver_options = Options()
    driver_options.set_preference("browser.download.folderList", 2)  # custom location
    driver_options.set_preference("browser.download.dir", download_dir)
    driver_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")  # adjust MIME type
    driver_options.set_preference("pdfjs.disabled", True)  # disable built-in viewer


    # Creates Driver and requests the url page 
    driver = webdriver.Firefox(options=driver_options)
    driver.get(link)

    return driver 

'''

def getExcel(driver):
    # Get html elements that have tag a 
    links = driver.find_elements(By.TAG_NAME, "a")
    print("Visible links:")
    for a in links:
        print("-", a.text)

    time.sleep(2)
    # Find element with download text
    link = driver.find_element(By.LINK_TEXT, "Download ratings")

    
    # Clicks on link
    driver.execute_script("arguments[0].click();", link)

    time.sleep(2)

    driver.close()

    # Retrieves Excel File 
    excel_files = glob.glob(os.path.join(download_dir, "*.xlsx"))
    # Sorts by most recent 
    excel_files.sort(key=os.path.getmtime)

    return excel_files[-1]

if __name__ == "__main__":
    # Finds path to download 
    download_dir = os.path.abspath("downloads")

    url = "https://tef2023.officeforstudents.org.uk/"

    browser_driver = helper.createDriver(url)

    path = getExcel(browser_driver)

    conversion_to_csv(path)




