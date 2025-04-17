from src.dataset_scripts.companies_house import trustees
from unittest.mock import patch, MagicMock
import pandas as pd
import pytest

@patch("dataset_scripts.companies_house.trustees.requests.get")
def test_get_officers_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            { "name": "John Doe",
            "officer_role": "director",
            "appointed_on": "2020-01-01"
            }
        ]
    }

    mock_get.return_value = mock_response

    result = trustees.get_officers("12345678")
    assert result == mock_response.json.return_value["items"]


@patch("dataset_scripts.companies_house.trustees.time.sleep") 
@patch("builtins.print")
@patch("dataset_scripts.companies_house.trustees.requests.get")
def test_get_officers_rate_limit(mock_get, mock_print, mock_sleep):

    mock_response_429 = MagicMock()
    mock_response_429.status_code = 429

    mock_response_200 = MagicMock()
    mock_response_200.status_code = 200
    mock_response_200.json.return_value = {
        "items": [
            { "name": "John Doe",
            "officer_role": "director",
            "appointed_on": "2020-01-01"
            }
        ]
    }

    mock_get.side_effect = [mock_response_429, mock_response_200]

    result = trustees.get_officers("12345678")

    mock_print.assert_called_with("Rate limit exceeded, waiting")
    mock_sleep.assert_called_once_with(60)

    assert result == mock_response_200.json.return_value["items"]
    assert mock_sleep.called


@patch("builtins.print")
@patch("dataset_scripts.companies_house.trustees.requests.get")
def test_get_officers_unauthorised(mock_get, mock_print):

    mock_response = MagicMock()
    mock_response.status_code = 401

    mock_get.return_value = mock_response

    with pytest.raises(SystemExit):
        trustees.get_officers("12345678")

    mock_print.assert_called_with("Unauthorized: Can't gain access")


@patch("dataset_scripts.companies_house.trustees.get_officers")
def test_process_rows(mock_get_officers):

    mock_get_officers.return_value = [
        {
            "name": "John Doe",
            "officer_role": "director",
            "appointed_on": "2020-01-01"
        }
    ]
    
    data = pd.DataFrame([{
        "Companies house number": "12345678",
        "UKPRN": "10012345"
    }])

    result = trustees.process_rows(data)

    assert len(result) == 1
    assert result[0]["Name"] == "John Doe"
    assert result[0]["Companies House Number"] == "12345678"
    assert result[0]["UKPRN"] == "10012345"
    assert result[0]["Officer Role"] == "director"
    assert result[0]["Appointed On"] == "2020-01-01" 
    assert result[0]["Resigned On"] == "N/A"


@patch("helper_scripts.helper.filePath") 
def test_save_data(mock_file_path, tmp_path):
    data = [
        {
            "Companies House Number": "12345678",
            "UKPRN": "10012345",
            "Name": "John Doe",
            "Officer Role": "director",
            "Appointed On": "2020-01-01",
            "Resigned On": "N/A"
        }
    ]

    file_path = tmp_path / "trust_officers.csv"
    mock_file_path.return_value = file_path

    trustees.save_data(data)

    df = pd.read_csv(file_path)
    assert df.iloc[0]["Name"] == "John Doe"
    assert str(df.iloc[0]["Companies House Number"]) == "12345678"
    assert str(df.iloc[0]["UKPRN"]) == "10012345"