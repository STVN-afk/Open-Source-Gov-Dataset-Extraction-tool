from src.dataset_scripts.nomis import employment
from src.dataset_scripts.nomis import ethnicities
from src.dataset_scripts.nomis import national_averages
from src.dataset_scripts.nomis import population_estimate
from src.dataset_scripts.nomis import population
from src.dataset_scripts.nomis import unemployment

import os
from unittest.mock import patch, MagicMock
import pandas as pd
import helper_scripts.helper as helper
import datetime


@patch("src.dataset_scripts.nomis.ethnicities.requests.get")
def test_ethnicities_conversion_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200

    input = helper.filePath("nomis_ethnicities_test_file.csv", "tests/test_datasets")
    assert os.path.exists(input), f"Input file {input} does not exist."

    with open(input, "r") as f:
        mock_response.text = f.read()

    mock_get.return_value = mock_response

    ethnicities.Ethnicities_Conversion()

    output = helper.filePath(f"EthnicGroup_{helper.getDate()}.csv", ".csvs")
    #assert output.exists()
    df = pd.read_csv(output)

    assert "GEOGRAPHY_NAME" in df.columns
    assert "Asian" in df.columns
    assert df["GEOGRAPHY_NAME"].nunique() == len(df)

    os.remove(output)

@patch("src.dataset_scripts.nomis.national_averages.requests.get")
def test_national_averages_conversion_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200

    input = helper.filePath("nomis_averages_test_file.csv", "tests/test_datasets")
    assert os.path.exists(input), f"Input file {input} does not exist."

    with open(input, "r") as f:
        mock_response.text = f.read()

    mock_get.return_value = mock_response

    national_averages.National_Averages_Conversion()

    output = helper.filePath(f"NationalAverages_{helper.getDate()}.csv", ".csvs")
    df = pd.read_csv(output)

    assert "VARIABLE_NAME" in df.columns
    assert "percent" in df.columns
    assert df["VARIABLE_NAME"].nunique() == len(df)

    os.remove(output)


@patch("src.dataset_scripts.nomis.population.requests.get")
def test_population_conversion_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200

    input = helper.filePath("nomis_population_test_file.csv", "tests/test_datasets")
    assert os.path.exists(input), f"Input file {input} does not exist."

    with open(input, "r") as f:
        mock_response.text = f.read()

    mock_get.return_value = mock_response

    population.Population_Conversion()

    output = helper.filePath(f"Population_{helper.getDate()}.csv", ".csvs")
    df = pd.read_csv(output)

    assert "local authority" in df.columns
    assert "numbers" in df.columns
    assert df["local authority"].nunique() == len(df)

    os.remove(output)

@patch("src.dataset_scripts.nomis.population_estimate.requests.get")
def test_population_estimation_conversion_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200

    input = helper.filePath("nomis_population_estimate_test_file.csv", "tests/test_datasets")
    assert os.path.exists(input), f"Input file {input} does not exist."

    with open(input, "r") as f:
        mock_response.text = f.read()

    mock_get.return_value = mock_response

    population_estimate.Population_Estimate_Conversion(1)

    output = helper.filePath(f"PopulationEstimates_Male_{helper.getDate()}.csv", ".csvs")
    df = pd.read_csv(output)

    assert "DATE_NAME" in df.columns
    assert "Gender" in df.columns
    assert "GEOGRAPHY_NAME" in df.columns
    assert "Age 2" in df.columns
    assert df["GEOGRAPHY_NAME"].nunique() == len(df)

    os.remove(output)


@patch("src.dataset_scripts.nomis.unemployment.requests.get")
def test_unemployment_conversion_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200

    input = helper.filePath("nomis_unemployment_test_file.csv", "tests/test_datasets")
    assert os.path.exists(input), f"Input file {input} does not exist."

    with open(input, "r") as f:
        mock_response.text = f.read()

    mock_get.return_value = mock_response

    unemployment.Unemployment_Conversion()

    output = helper.filePath(f"Unemployed_{helper.getDate()}.csv", ".csvs")
    df = pd.read_csv(output)

    assert "Local Authority" in df.columns
    assert "numbers" in df.columns
    assert "%" in df.columns
    assert df["Local Authority"].nunique() == len(df)

    os.remove(output)

@patch("src.dataset_scripts.nomis.employment.requests.get")
def test_employment_conversion_success(mock_get):
    mock_response1 = MagicMock()
    mock_response2 = MagicMock()
    mock_response1.status_code = 200
    mock_response2.status_code = 200

    input1 = helper.filePath("nomis_employment_1_test_file.csv", "tests/test_datasets")
    input2 = helper.filePath("nomis_employment_2_test_file.csv", "tests/test_datasets")


    assert os.path.exists(input1), f"Input file {input1} does not exist."
    assert os.path.exists(input2), f"Input file {input2} does not exist."


    with open(input1, "r") as f:
        mock_response1.text = f.read()

    with open(input2, "r") as f:
        mock_response2.text = f.read()

    mock_get.side_effect = [mock_response1, mock_response2]

    employment.Employment_Conversion()

    output = helper.filePath(f"Employment_{helper.getDate()}.csv", ".csvs")
    df = pd.read_csv(output)

    assert "Local Authority" in df.columns
    assert "numbers" in df.columns
    assert "%" in df.columns
    assert df["Local Authority"].nunique() == len(df)

    os.remove(output)


def test_correct_date():
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    assert helper.getDate() == date,"Wrong Date"

    print("Correct Date")