import sys

import os
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()

options.headless = True

cwd = os.getcwd()
path = cwd + '/chromedriver.exe'
os.environ['PATH'] += path
zips = open("Germany_zipcodes.txt", 'r')
zips = zips.readlines()
zipcodes = ''
for item in zips:
    zipcodes += item
zipcodes = zipcodes.split(",")

for i, item in enumerate(zipcodes):
    zipcodes[i] = item.strip()

print(zipcodes)
actual_Zip_codes = []
for zipcode in zipcodes:
    for x in range(1, 3):
        for y in range(1, 10):
            try:
                print(zipcode)
                print(x,y)
                driver = webdriver.Chrome(options=options)
                driver.get("https://www.immowelt.de/#")
                HomeMultipleChoice = driver.find_element(By.ID, "spanSearchWhat")
                ZipcodeInput = driver.find_element(By.ID, "tbLocationInput")
                seekBTN = driver.find_element(By.ID, "btnSearchSubmit")
                HomeMultipleChoice.click()
                division = driver.find_element(By.XPATH, f'//*[@id="divSearchWhatFlyout"]/div[{x}]/ul/li[{y}]')
                division.click()
                ZipcodeInput.send_keys(zipcode)
                seekBTN.click()
                driver.implicitly_wait(5)
                time.sleep(0.4)
                url = driver.current_url
                print(url)
                if url != "https://www.immowelt.de/#":
                    actual_Zip_codes.append(zipcode)
            except:
                pass
            break
        break

print("actual zipcodes = ", actual_Zip_codes)

fhand2 = open('actual_zipcodes_Germany.txt', 'w')
for line in actual_Zip_codes:
    fhand2.write(f"{line} \n")

fhand2.close()

