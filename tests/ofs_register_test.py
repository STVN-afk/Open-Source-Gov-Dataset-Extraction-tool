from src.dataset_scripts import ofs_register
import os

def test_ofs_register():

    url = ("https://register-api.officeforstudents.org.uk/api/Download/")
    filename = 'testing_file.csv'

    csv_dir = os.path.abspath(".csvs")
    full_path = os.path.join(csv_dir, filename)

    ofs_register.ofs_register(url, full_path)

    assert os.path.exists(full_path), "CSV file was not downloaded"
    assert full_path.endswith('.csv'), "Filename does not end with .csv"

    os.remove(full_path)
