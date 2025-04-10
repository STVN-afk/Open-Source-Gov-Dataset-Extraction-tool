import os
import requests
import pandas as pd 



def ofs_register(url, final_csv_path):
    response = requests.get(url)

    with open("ofs.xlsx", "wb") as f:
        f.write(response.content)
    
    # keep_default_na=False makes sure that 'None' values don't become empty
    excel = pd.read_excel("ofs.xlsx", sheet_name="Register", keep_default_na=False)
    
    # encoding stops weird encoding errors, when cells say 'None' na_rep keeps them this way
    excel.to_csv("ofs.csv", index=False, encoding="utf-8-sig", na_rep='None')

    # remove first two rows of csv, save
    csv = pd.read_csv("ofs.csv", skiprows=2, encoding="utf-8-sig")
    csv.to_csv(final_csv_path, index=False, encoding="utf-8-sig", na_rep='None')

    # remove the unneeded excel and csv file
    os.remove("ofs.xlsx")
    os.remove("ofs.csv")

    # Find top row in a better way





if __name__ == "__main__":
    
    url = "https://register-api.officeforstudents.org.uk/api/Download/"

    csv_name = "ofs_register.csv"
    csv_dir = os.path.abspath(".csvs")
    full_path = os.path.join(csv_dir, csv_name)

    ofs_register(url, full_path)