# Open Source Gov Dataset Extraction Tool

## Introduction 
Developed by Steve Van and Sam Horrell during the Workplace Insights Placement with the Department for Education (DfE) in Sheffield, this tool automates the download, cleansing, formatting and extraction of key open government datasets.

### Supported Datasets
This tool supports automation for the following open data sources:
- [Payment Practices](https://check-payment-practices.service.gov.uk/export/)
- [TEF Outcomes 2023](https://tef2023.officeforstudents.org.uk/)
- [Ofs Register](https://www.officeforstudents.org.uk/for-providers/regulatory-resources/the-ofs-register/#/)
- [CQC](https://www.cqc.org.uk/about-us/transparency/using-cqc-data)
- [Constituency & MP](https://developer.parliament.uk/)
- [Company House - Using API to filter and extract datasets](https://developer.company-information.service.gov.uk/overview)
- [Nomis - Using API to extract datasets and convert to correct format](https://www.nomisweb.co.uk/api/v01/help)

Each dataset is programmatically downloaded, formatted and saved locally, making it easier to process, analyze, and use for research or operational needs.

# Prerequisites
To use the Open Source Gov Dataset Extraction Tool, ensure you have the following installed:
- Python 3.8+, our Backend used for creating the scripts.
- Necessary Python Libraries, Download using Makefile
- Web Browser + Driver (Selenium), Used in simulating the webpage for Tef 2023. Currently using Firefox browser for our driver.
- API Keys, required by some datasets to request and access data. You will need to register and generate API keys for the following services:
    - [Constituency & MP](https://developer.parliament.uk/)
    - [Company House](https://developer.company-information.service.gov.uk/overview)
  
 Store your keys securely using a .env file and load them in your scripts using the python-dotenv package to keep your credentials private.

# Installation 
uses pytest 8.3.5 to run tests.
A makefile has been provided to run tests and download dependencies.
<Talk about Makefile and downloads here>

# Usage Instructions + Explanations
 ### Payment Practices
 This script automates the download of CSV files from the UK Government's [Payment Practices](https://check-payment-practices.service.gov.uk/export/) website. <br/>
 This script uses the urllib module to access the url link to the .csv file and saves it within the .csvs folder.

 To execute script, run the following command in the terminal:
  <pre> python .\src\dataset_scripts\payment_practices.py </pre>
 or f5 on the script in an IDE

 ### TEF Outcomes 2023
  TBA

### Ofs Register 
This script automates the download of CSV files from the Office for Students's [Ofs Register](https://www.officeforstudents.org.uk/for-providers/regulatory-resources/the-ofs-register/#/) website. <br/>
This script uses the request package to retrieve the unformatted file from the site and then formats it into a csv file which is saved to the .csvs file.

 To execute script, run the following command in the terminal:
  <pre> python .\src\dataset_scripts\ofs_register.py </pre>
 or f5 on the script in an IDE

 ### CQC 
 This script automates the download of CSV files from the Care Quality Commission's [CQC](https://www.cqc.org.uk/about-us/transparency/using-cqc-data) website. <br/>
 This script uses the uses the datetime package to get the current date and creates url links to the respective buttons on the page. If found, then it will download the 
 file and save it locally and then format it into a csv file. If not found, then the button has not been updated with the new dataset so it is ignored.

 To execute script, run the following command in the terminal:
   <pre> python .\src\dataset_scripts\CQC.py </pre>
 or f5 on the script in an IDE. CQC links may update so to test actual functionality of the script, run the pytest.

 ### Constituency & MP 
 TBD

 ### Company House 
 2 Scripts 

 ### Nomis 
 TBD

 # Contact 
 For questions, feedback, or assistance, you can reach out to:

[Sam Horrell](https://github.com/shorrell1) <br/>
[Steve Van](https://github.com/STVN-afk)

 


 


 



