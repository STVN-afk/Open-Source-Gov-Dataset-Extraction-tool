from urllib.request import urlretrieve
import pandas as pd 
import urllib
import os

def retrieve(url, filename):
    csv_dir = os.path.abspath(".csvs")
    urlretrieve(url, os.path.join(csv_dir,filename))
    return filename 

url = ("https://check-payment-practices.service.gov.uk/export/csv/")
filename = "payment_practice.csv"
retrieve(url, filename)

def conversion_to_csv(filename):
    file = pd.read_excel(filename)
    file.to_csv(filename, index=False, quotechar="'")


    