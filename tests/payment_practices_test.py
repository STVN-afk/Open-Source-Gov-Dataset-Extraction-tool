from src.dataset_scripts import payment_practices
import os


def test_download():

    url = ("https://check-payment-practices.service.gov.uk/export/csv/")
    filename = 'test_file.csv'

    csv_dir = os.path.abspath(".csvs")
    full_path = os.path.join(csv_dir, filename)

    payment_practices.download(url, full_path)

    assert os.path.exists(full_path), "CSV file was not downloaded"
    assert full_path.endswith('.csv'), "Filename does not end with .csv"

    os.remove(full_path)
