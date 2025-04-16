from src.dataset_scripts.parliament import parliament
import os
import csv



def test_fetch_mps():

    url = "https://members-api.parliament.uk/api/Members/Search"

    mp_data, num = parliament.fetch_20_mps(url, [], 10)

    assert len(mp_data) == 20
    assert num == 20


def test_fetch_mps_out_of_range():

    url = "https://members-api.parliament.uk/api/Members/Search"

    mp_data, num = parliament.fetch_20_mps(url, [], 40)

    assert mp_data == []
    assert num == 0

# Testing it collects all MPs (assumes no more than 10 vacant seats)
def test_fetch_all_mps():

    url = "https://members-api.parliament.uk/api/Members/Search"

    mp_data = parliament.fetch_mps(url)

    assert len(mp_data) > 640


def test_convert_to_csv():

    mp_data = [['John Smith', 'Sheffield Hallam'], ['Jane Doe', 'Warrington South']]

    filename = "test.csv"

    csv_dir = os.path.abspath(".csvs")
    full_path = os.path.join(csv_dir, filename)

    parliament.convert_to_csv(mp_data, full_path)

    assert os.path.exists(full_path), "CSV file was not downloaded"
    assert full_path.endswith('.csv'), "Filename does not end with .csv"

    os.remove(full_path)

def test_as_a_whole():

    url = "https://members-api.parliament.uk/api/Members/Search"

    mp_data = parliament.fetch_mps(url)

    filename = "parliament.csv"

    csv_dir = os.path.abspath(".csvs")
    full_path = os.path.join(csv_dir, filename)

    parliament.convert_to_csv(mp_data, full_path)

    assert os.path.exists(full_path), "CSV file was not downloaded"
    assert full_path.endswith('.csv'), "Filename does not end with .csv"


    with open(full_path) as f:
        data = list(csv.reader(f))

    assert len(data) > 640

    os.remove(full_path)