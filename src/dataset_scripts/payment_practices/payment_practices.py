from urllib.request import urlretrieve
from helper_scripts import helper
import os
 
def download(url, filename):

    '''Downloads the information at a given to a file

    Args:
        url (string): URL of data
        filename(string): Name/Path of the file
    '''

    urlretrieve(url, filename)
 
if __name__ == "__main__":
    url = ("https://check-payment-practices.service.gov.uk/export/csv/")
    filename = "payment_practises.csv"
 
    file_path = helper.filePath(filename, ".csvs")

    download(url, file_path)