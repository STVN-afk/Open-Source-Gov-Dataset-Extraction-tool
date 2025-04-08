from urllib.request import urlretrieve

def download(url, filename):
    urlretrieve(url, filename)

if __name__ == "__main__":
    url = ("https://check-payment-practices.service.gov.uk/export/csv/")
    filename = "payment_practise.csv"
    download(url, filename)