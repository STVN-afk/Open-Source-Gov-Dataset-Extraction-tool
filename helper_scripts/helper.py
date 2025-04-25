from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import datetime
import os

def createDriver(link):
    # Preferences
    download_dir = os.path.abspath("downloads")

    driver_options = Options()

    driver_options.add_argument("--headless")

    driver_options.set_preference("browser.download.folderList", 2)  # custom location
    driver_options.set_preference("browser.download.dir", download_dir)
    driver_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")  # adjust MIME type
    driver_options.set_preference("pdfjs.disabled", True)  # disable built-in viewer


    # Creates Driver and requests the url page 
    driver = webdriver.Firefox(options=driver_options)
    driver.get(link)

    return driver 

# Returns the path for any file
def filePath(name, folder): 
    dir = os.path.abspath(folder)
    full_path = os.path.join(dir, name)
    return full_path

def getDate():
    '''
        DESCRIPTION:
            Retrieves the Current Date when the script was run.
    '''

    date = datetime.datetime.now()
    formatted_date = date.strftime("%d-%m-%Y")
    return formatted_date