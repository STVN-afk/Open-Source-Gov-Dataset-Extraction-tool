from urllib.request import urlretrieve


def retrieve(url, filename):
    urlretrieve(url, filename)

url = ("https://check-payment-practices.service.gov.uk/export/csv/")
filename = "payment_practise.csv"
retrieve(url, filename)