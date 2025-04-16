from src.dataset_scripts import proprietors
from helper_scripts import helper
from unittest.mock import patch, MagicMock
import pytest

def test_filter_rows():
    input = helper.filePath("proprietors_test_file.csv", "tests/test_datasets")

    filtered = proprietors.filter_rows(input)

    assert len(filtered) == 2
    assert all(filtered['PropsName'].notna())

@patch("dataset_scripts.proprietors.requests.get")
def test_fetch_company_match(mock_get): 

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {"title": "ASTRAZENECA PLC"}
        ]
    }

    mock_get.return_value = mock_response

    assert proprietors.fetch_company("ASTRAZENECA PLC".lower()) is True

@patch("dataset_scripts.proprietors.requests.get")
def test_fetch_company_doesnt_match(mock_get): 

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {"title": "ASTRAZENECA PLC"}
        ]
    }

    mock_get.return_value = mock_response

    assert proprietors.fetch_company("ASTRAZENECA  PLC".lower()) is False

@patch("builtins.print")
@patch("dataset_scripts.proprietors.requests.get")
def test_fetch_company_unauthorised(mock_get, mock_print):

    mock_response = MagicMock()
    mock_response.status_code = 401

    mock_get.return_value = mock_response

    with pytest.raises(SystemExit):
        proprietors.fetch_company("Company")

    mock_print.assert_called_with("Unauthorized: Can't gain access")

@patch("dataset_scripts.proprietors.time.sleep") 
@patch("builtins.print")
@patch("dataset_scripts.proprietors.requests.get")
def test_fetch_company_rate_limit(mock_get, mock_print, mock_sleep):

    mock_response_429 = MagicMock()
    mock_response_429.status_code = 429

    mock_response_200 = MagicMock()
    mock_response_200.status_code = 200
    mock_response_200.json.return_value = {
        "items": [{"title": "ASTRAZENECA PLC"}]
    }

    mock_get.side_effect = [mock_response_429, mock_response_200]

    assert proprietors.fetch_company("ASTRAZENECA PLC".lower()) is True

    mock_print.assert_called_with("Rate limit exceeded, waiting")
    mock_sleep.assert_called_once_with(60)
