import os
from unittest.mock import patch, MagicMock
import pandas as pd
import helper_scripts.helper as helper
from src.dataset_scripts.nomis import Nomis

@patch("dataset_scripts.nomis.Nomis.requests.get") 
def test_ethnicities_conversion_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200

    input = helper.filePath("nomis_ethnicities_test_file.csv", "tests/test_datasets")
    assert os.path.exists(input), f"Input file {input} does not exist."
    
    with open(input, "r") as f:
        mock_response.text = f.read()

    mock_get.return_value = mock_response
    
    Nomis.Ethnicities_Conversion()

    output = helper.filePath(f"EthnicGroup_{Nomis.getDate()}.csv", ".csvs")
    #assert output.exists()
    df = pd.read_csv(output)

    assert "GEOGRAPHY_NAME" in df.columns
    assert "Asian" in df.columns
    assert df["GEOGRAPHY_NAME"].nunique() == len(df)