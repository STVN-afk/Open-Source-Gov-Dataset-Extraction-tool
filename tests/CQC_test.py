from src.dataset_scripts import CQC 
import os, datetime
import pytest
import pandas as pd
from unittest.mock import patch, mock_open, MagicMock

@patch("builtins.open", new_callable=mock_open)
@patch("os.path.basename")
@patch("requests.get") 
@patch("pandas.read_csv")
@patch("pandas.ExcelFile")  


def test_CQC_mock_download(mock_excel,mock_readcsv,mock_requests_get,mock_basename,mocker):

    urls = [
        "https://testing.com/examplecsv.csv",
        "https://testing.com/exampleods.ods",
        "https://testing.com/invalidods.ods"
    ]
    
    mock_basename.side_effect = lambda url: url.split("/")[-1]
    mock_readcsv.return_value = pd.DataFrame({"col1": [1, 2]})

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"Dummy ODS file content"

    mock_requests_get.side_effect = [
        mock_response,  # Success for data.ods
        MagicMock(status_code=404)  # 404 for missing.ods
    ]

    mock_excel_file = MagicMock()
    mock_excel_file.sheet_names = ["README", "Sheet1"]
    mock_excel_file.parse.return_value = pd.DataFrame({"colA": [10, 20]})
    mock_excel.return_value = mock_excel_file

    CQC.downloadFiles(urls)

    # Checks if read_csv was called
    assert mock_readcsv.called

    # Checks if requests.get was called twice
    assert mock_requests_get.call_count == 2

    # Checks if excelFile was Called
    assert mock_excel.called

    # Checks if parse was called.
    assert mock_excel_file.parse.called

def test_CQC_check_current_date():
    urls = CQC.geturls()
    date_format = datetime.datetime.now().strftime("%Y-%m/%d_%B_%Y")
    deactivated_format = date_format.replace("_","%20")

    for url in urls:
        print("url is " + url)
        assert str(date_format) in url or str(deactivated_format) in url, f"URL does not match current date"

    print("All urls match with the current date")
            

if __name__ == "__main__":
    test_CQC_check_current_date()
    test_CQC_mock_download()





