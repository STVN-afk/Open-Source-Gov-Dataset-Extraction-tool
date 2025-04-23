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
- make required, used to run the automatic download and import
  
 Store your keys securely using a .env file and load them in your scripts using the python-dotenv package to keep your credentials private.

# Installation 
uses pytest 8.3.5 to run tests.
A makefile has been provided to run tests and download dependencies. <br/>

To install all required dependencies, run the following in the terminal:
<pre> make install </pre>

To setup subdirectories needed for some of the scripts, run the following in the terminal:
<pre> make setup-dirs </pre>

To run Tests, run the following in the terminal:
<pre> make test </pre>

All Dependencies can be found in the requirements.txt file



<Talk about Makefile and downloads here>

# Usage Instructions + Explanations
 ### Payment Practices
 This script automates the download of CSV files from the UK Government's [Payment Practices](https://check-payment-practices.service.gov.uk/export/) website. <br/>
 This script uses the urllib module to access the url link to the .csv file and saves it within the .csvs folder.

 To execute script, run the following command in the terminal:
  <pre> python .\src\dataset_scripts\payment_practices\payment_practices.py </pre>
 or f5 on the script in an IDE

 ### TEF Outcomes 2023
  This script automates teh download of CSV files from TEF's [Outcomes 2023](https://tef2023.officeforstudents.org.uk/) website. <br/>
  This script uses Selenium to create a browser automation tool to simulate a click of the button on the webpage since the link is only generated after button click. <br/>
  The file returned is a xslx file (excel) which is then converted to an excel file through numpy. However, this xslx could not be read in natively therefore we needed the xlwings module to resave it as an excel file which can then be manipulated to return a csv file.

  To execute script, run the following command in the terminal:
  <pre> python .\src\dataset_scripts\teaching_excellence_framework\tef_2024.py</pre>
 or f5 on the script in an IDE

### Ofs Register 
This script automates the download of CSV files from the Office for Students's [Ofs Register](https://www.officeforstudents.org.uk/for-providers/regulatory-resources/the-ofs-register/#/) website. <br/>
This script uses the request package to retrieve the unformatted file from the site and then formats it into a csv file which is saved to the .csvs file.

 To execute script, run the following command in the terminal:
  <pre> python .\src\dataset_scripts\office_for_students\ofs_register.py</pre>
 or f5 on the script in an IDE

 ### CQC 
 This script automates the download of CSV files from the Care Quality Commission's [CQC](https://www.cqc.org.uk/about-us/transparency/using-cqc-data) website. <br/>
 This script uses the uses the datetime package to get the current date and creates url links to the respective buttons on the page. If found, then it will download the 
 file and save it locally and then format it into a csv file. If not found, then the button has not been updated with the new dataset so it is ignored.

 To execute script, run the following command in the terminal:
   <pre> python .\src\dataset_scripts\care_quality_commission\CQC.py </pre>
 or f5 on the script in an IDE. CQC links may update so to test actual functionality of the script, run the pytest.

 ### Constituency & MP 
 This script automates the download of CSV files from the UK Parliments [Constituency & MP Dataset](https://developer.parliament.uk/) using an API Key. <br/>
 It uses a for loop to iteratively loop through 20 MP's and their Constituencies and saving it into a list until there are no more MP's in which it is then converted into a suitable csv file for usage. <br/>
 Rate is set to 20 since the UK Parliment's API can only return 20 values at a time.

 To execute script, run the following command in the terminal:
   <pre> python .\src\dataset_scripts\parliament\parliament.py </pre>
 or f5 on the script in an IDE. CQC links may update so to test actual functionality of the script, run the pytest.

 ### Company House 
 2 Scripts automating the download of csv files for the parent companies and trustees from the [Companies House](https://developer.company-information.service.gov.uk/overview) website using an API Key. 

 The script for parent companies returns the URN and company house no for each parent company in the dataset. <br/>
 This script recursively calls itself allowing for the full history of each trust and their parentage. <br/>
 This script also sends 500 requests every 5 minutes due to API limitations.

  To execute script, run the following command in the terminal:
   <pre> python .\src\dataset_scripts\companies_house\parent_companies.py</pre>
 or f5 on the script in an IDE.

 The script for trustees returns all the officers for a single trustee, whether they have retired or not and their role. <br/>
 This script recursively calls itself allowing for the full history of each officer in a trust. <br/>
 This script also sends 500 requests every 5 minutes due to API limitations.

  To execute script, run the following command in the terminal:
   <pre> python .\src\dataset_scripts\companies_house\trustees.py</pre>
 or f5 on the script in an IDE.

 ### Nomis 
 This Script Automates the download of CSV files from the Nomi's [Dataset](https://www.nomisweb.co.uk/sources) Website for the Following:
 - Employment
 - Ethnicity
 - National Averages
 - Population
 - Population Estimates
 - Unemployed

Each function executes a specific API Call to the Nomis Website to request a dataset, which is then cleansed and formatted before being saved into a csv file for usage.
This script also uses the datetime package to get the current date to save the filename in a specific structure. 


 To execute script, run the following command in the terminal:
   <pre> python .\src\dataset_scripts\nomis\Nomis.py </pre>
 or f5 on the script in an IDE.



 # Contact 
 For questions, feedback, or assistance, you can reach out to:

[Sam Horrell](https://github.com/shorrell1) <br/>
[Steve Van](https://github.com/STVN-afk)

 


 


 



