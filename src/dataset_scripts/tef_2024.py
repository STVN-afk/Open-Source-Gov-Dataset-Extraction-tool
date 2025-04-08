import os
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("https://tef2023.officeforstudents.org.uk")
print(driver.title)

links = driver.find_elements(By.TAG_NAME, "a")
print("Visible links:")
for a in links:
    print("-", a.text)

link = driver.find_element(By.LINK_TEXT, "Download ratings")

driver.execute_script("arguments[0].click();", link)