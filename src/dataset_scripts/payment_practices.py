from urllib.request import urlretrieve
import os
 
def download(url, filename):
    urlretrieve(url, filename)
    return filename 
 
if __name__ == "__main__":
    url = ("https://check-payment-practices.service.gov.uk/export/csv/")
    filename = "payment_practise.csv"

    csv_dir = os.path.abspath(".csvs")
    full_path = os.path.join(csv_dir, filename)
 
    download(url, filename)