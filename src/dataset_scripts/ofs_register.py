import os
import requests
import pandas as pd

def find_data_start(file_path, known_header="Provider’s legal name"):

    '''Finds the start of the data (first few lines are irrelevant)
        Looks for "Provider's legal name" (a column) and skips to that line
        If it can't find the text, it returns the first line

    Args:
        file_path (string): The location of the csv file
        known_header (string): A column name to search for

    Returns:
        i (int): The line at which the data starts
    '''

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        for i, line in enumerate(f):
            if known_header in line:
                return i
    return 0 


def ofs_register(url, final_csv_path):

    '''Downloads the data and converts to a csv with unneeded data removed
        Uses find_data_start to find where to cut off the csv at
        Removes unneeded data at the end

    Args:
        url (string): URL to download data from
        final_csv_path (string): Location to save csv at
    '''

    response = requests.get(url)

    with open("ofs.xlsx", "wb") as f:
        f.write(response.content)

    excel = pd.read_excel("ofs.xlsx", sheet_name="Register", keep_default_na=False)
    excel.to_csv("ofs.csv", index=False, encoding="utf-8-sig", na_rep='None')

    start_row = find_data_start("ofs.csv")

    csv = pd.read_csv("ofs.csv", skiprows=start_row, encoding="utf-8-sig")
    csv.to_csv(final_csv_path, index=False, encoding="utf-8-sig", na_rep='None')

    os.remove("ofs.xlsx")
    os.remove("ofs.csv")


if __name__ == "__main__":
    url = "https://register-api.officeforstudents.org.uk/api/Download/"
    csv_name = "ofs_register.csv"
    csv_dir = os.path.abspath(".csvs")
    full_path = os.path.join(csv_dir, csv_name)

    ofs_register(url, full_path)