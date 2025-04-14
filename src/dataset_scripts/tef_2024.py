from selenium.webdriver.common.by import By
from helper_scripts import helper
import pandas as pd 
import glob, time, os 
import xlwings as xw

'''
Removed as Helper script has function to create driver making it redundant for below
Remove comments if the creation of the driver is wanted on the script itself alongside the function

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

'''

def conversion_to_csv(filename):

    '''
        DESCRIPTION:
        Checks if the file file can be read using the pd module, if there is an issue, that means 
        the excel file cannot be read using openpyxl (pd default engine). Afterwards, it will read the 
        file and convert it into a csv file at the path given and deletes the 

        PROBLEMS:
        The downloaded xslx cannot be read straight from the download due to style errors. To resolve this,
        The xlwings module (needs to be downloaded) is used to open the file using excel in the case 
        it cannot be read by openpyxl and resaving the file using excel's default format which can then 
        be read in by the script.

        Currently the only workaround is using the xlwings module for this specific excel workbook.

        PARAMETERS:
        filename (str): The path which leads to the downloaded xslx file.

        RETURNS:
        csv_path (str): The path in which the csv file is located.

    '''

    while True:
        # Tries to read Excel file 
        try:
            file = pd.read_excel(filename, engine= "openpyxl")
        except Exception as e:
            path2 = filename 
            print(f"Failed to open workbook; error: {e}")
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

    # Only used for testing, if statement can be deleted if necessary

    if filename != str(os.path.abspath("tests/test_datasets/file_example_XLSX_50.xlsx")):
        os.remove(filename)

    return csv_path

'''
If Driver needs to be created within the script, remove the comments.

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
    '''
        DESCRIPTION:
        Uses the selenium package to search for all tags on the html page that are hyperlinks.
        It then finds the specific link, Download Ratings and simulates a click which causes it to 
        download the xslx file from the site. From there, using the glob package, we find the most 
        recent download in the downloads folder and return it.

        PROBLEMS:
        Tried using the requests package with the hyperlink to get the xslx file, however after implementation 
        it returned empty. We believe it is because the website requires you to click on the linked element to
        the hyperlink through javascript in order to download which is why selenium is implemented to simulate 
        automate web browser interaction. 

        Script would try to instantly return the file although it was still downloading which caused errors.
        To resolve this issue, the time package was imported to sleep the script until the download was complete.

        PARAMETERS:
        driver (webdriver): Used to automate the interaction on the page in order to download the file.

        RETURNS:
        excel_files[-1] (str): Returns the path of the last downloaded file in the downloads folder.
    
    '''
    # Get html elements that have tag a 
    links = driver.find_elements(By.TAG_NAME, "a")
  
    time.sleep(2)
    # Find element with download text
    link = driver.find_element(By.LINK_TEXT, "Download ratings")

    # Clicks on link
    driver.execute_script("arguments[0].click();", link)

    time.sleep(2)

    driver.quit()

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




