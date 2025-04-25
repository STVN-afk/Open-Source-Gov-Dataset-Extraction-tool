from src.dataset_scripts.companies_house import parent_companies
from unittest.mock import patch, MagicMock
import pytest

@patch("src.dataset_scripts.companies_house.parent_companies.requests.get")
def test_fetch_parent_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "kind": "corporate-entity-person-with-significant-control",
                "ceased": False,
                "name": "Parent Corp Ltd"
            },
            {
                "kind": "individual-person-with-significant-control",
                "ceased": False,
            }
        ]
    }
    mock_get.return_value = mock_response

    result = parent_companies.fetch_parent("12345678")
    assert result["name"] == "Parent Corp Ltd"


@patch("dataset_scripts.companies_house.parent_companies.time.sleep")
@patch("builtins.print")
@patch("src.dataset_scripts.companies_house.parent_companies.requests.get")
def test_fetch_parent_rate_limit(mock_get, mock_print, mock_sleep):
    mock_response_429 = MagicMock(status_code=429)
    mock_response_200 = MagicMock()
    mock_response_200.status_code = 200
    mock_response_200.json.return_value = {
        "items": [
            {
                "kind": "corporate-entity-person-with-significant-control",
                "ceased": False,
                "name": "Retry Parent Ltd"
            }
        ]
    }

    mock_get.side_effect = [mock_response_429, mock_response_200]

    result = parent_companies.fetch_parent("12345678")

    mock_print.assert_called_with("Rate limit exceeded, waiting")
    mock_sleep.assert_called_once_with(60)
    assert result["name"] == "Retry Parent Ltd"


@patch("src.dataset_scripts.companies_house.parent_companies.requests.get")
@patch("builtins.print")
def test_fetch_parent_server_error(mock_print, mock_get):
    mock_response = MagicMock(status_code=502)
    mock_get.return_value = mock_response

    result = parent_companies.fetch_parent("12345678")
    assert result is None
    mock_print.assert_called_with("Skipping because of server issues")


@patch("src.dataset_scripts.companies_house.parent_companies.requests.get")
@patch("builtins.print")
def test_fetch_parent_unauthorized(mock_print, mock_get):
    mock_response = MagicMock(status_code=401)
    mock_get.return_value = mock_response

    with pytest.raises(SystemExit):
        parent_companies.fetch_parent("12345678")
    
    mock_print.assert_called_with("Unauthorized: Can't gain access")


@patch("src.dataset_scripts.companies_house.parent_companies.requests.get")
def test_fetch_parent_no_match(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {"kind": "individual-person-with-significant-control", "ceased": False},
            {"kind": "corporate-entity-person-with-significant-control", "ceased": True}
        ]
    }
    mock_get.return_value = mock_response

    result = parent_companies.fetch_parent("12345678")
    assert result is None


@patch("src.dataset_scripts.companies_house.parent_companies.fetch_parent")
def test_fetch_parents_recursive(mock_fetch_parent):

    mock_fetch_parent.side_effect = [
        {
            "name": "Parent Ltd",
            "identification": {
                "registration_number": "11111111",
                "country_registered": "England"
            }
        },
        {
            "name": "Ultimate Parent Ltd",
            "identification": {
                "registration_number": "22222222",
                "country_registered": "United Kingdom"
            }
        },
        None  
    ]

    academy_info = []
    result = parent_companies.fetch_parents(
        academy_info,
        subsidiary_id="00000000",
        ukprn="10012345"
    )

    assert len(result) == 2

    assert result[0]["Subsidiary ID"] == "00000000"
    assert result[0]["Company ID"] == "11111111"
    assert result[0]["Company Name"] == "Parent Ltd"
    assert result[0]["UKPRN"] == "10012345"
    assert result[0]["Country"] == "England"
    assert result[0]["Degrees Removed"] == 1

    assert result[1]["Subsidiary ID"] == "11111111"
    assert result[1]["Company ID"] == "22222222"
    assert result[1]["Company Name"] == "Ultimate Parent Ltd"
    assert result[1]["UKPRN"] == "10012345"
    assert result[1]["Country"] == "United Kingdom"
    assert result[1]["Degrees Removed"] == 2

