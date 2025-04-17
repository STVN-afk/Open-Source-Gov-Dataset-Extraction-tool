from src.dataset_scripts.nomis import Nomis
import pandas as pd
from unittest.mock import patch, MagicMock
import datetime, io

def test_correct_date():
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    assert Nomis.getDate() == date,"Wrong Date"

    print("Correct Date")


if __name__ == "__main__":
    test_correct_date()





