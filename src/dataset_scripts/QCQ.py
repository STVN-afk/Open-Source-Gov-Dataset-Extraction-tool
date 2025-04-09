from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import pandas as pd 
import time, os, urllib.parse
import pickle


# Finds path to download 
download_dir = os.path.abspath("downloads")
csv_dir = os.path.abspath(".csvs")

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

def conversion_from_ods_to_csv(filename):
    print("Starting Conversion")
    pd.read_excel(filename, engine="odf")

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
            
if __name__ == "__main__":                
    driver = createDriver()
    driver.get("https://www.cqc.org.uk/about-us/transparency/using-cqc-data")
    downloadFiles(driver)
    conversion_from_ods_to_csv("/home/student/Sheffield-Campus-Policy-/downloads/01_April_2025_Latest_ratings.ods")


