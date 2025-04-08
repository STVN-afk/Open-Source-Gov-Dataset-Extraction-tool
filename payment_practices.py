from urllib.request import urlretrieve
import os


def retrieve(url, filename):
    urlretrieve(url, filename)

url = ("https://check-payment-practices.service.gov.uk/export/csv/")
filename = "payment_practise.csv"
retrieve(url, filename)


def test_download():
    url = 'https://check-payment-practices.service.gov.uk/export/csv/'
    filename = 'test_file.csv'
    
    retrieve(url, filename)

    assert os.path.exists(filename), "CSV file was not downloaded"
    assert filename.endswith('.csv'), "Filename does not end with .csv"

    os.remove(filename)


test_download()