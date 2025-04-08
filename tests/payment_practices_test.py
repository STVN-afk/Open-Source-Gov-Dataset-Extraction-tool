from dataset_scripts import payment_practices
import os

def test_download():
 
    url = 'https://check-payment-practices.service.gov.uk/export/csv/'
    filename = 'test_file.csv'
 
    payment_practices.download(url, filename)
 
    assert os.path.exists(filename), "CSV file was not downloaded"
    assert filename.endswith('.csv'), "Filename does not end with .csv"
 
    os.remove(filename)

test_download()