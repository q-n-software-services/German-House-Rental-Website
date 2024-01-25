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
                page = requests.get(url)
                soup = BeautifulSoup(page.content, "html.parser")
                # fhand = open("page.html", 'w')
                # fhand.write(str(page.content))
                # print(str(soup))
                titles = soup.findAll('h2')
                details = soup.find_all("div", class_="KeyFacts-efbce")
                furtherDetails = soup.find_all("div", class_="IconFact-e8a23")
                backLinks = soup.findAll(True, {'class': ['mainSection-b22fb', 'noProject-eaed4']})

                for i in range(len(titles)):
                    print(i)
                    try:
                        titles[i] = str(titles[i]).split(">")[1].strip().split("<")[0].strip()
                        newDetails = {"price": str(details[i]).split('price">')[1].strip().split("<")[0].strip(),
                                      "area": str(details[i]).split('area">')[1].strip().split("<")[0].strip(),
                                      "rooms": str(details[i]).split('rooms">')[1].strip().split("<")[0].strip()}

                        newFurtherDetails = {
                            "location": str(furtherDetails[2 * i]).split('location</i><span>')[1].strip().split("<")[0].strip(),
                            "check": str(furtherDetails[(2 * i) + 1]).split('check</i><span>')[1].strip().split("<")[0].strip()}

                        newBacklinks = {"link": str(backLinks[i]).split('<a class="mainSection-b22fb noProject-eaed4" href="')[
                            1].strip().split('"')[0].strip(),
                                        "image": str(backLinks[i]).split('<picture><source data-srcset="')[1].strip().split('"')[0].strip()}

                        print('title : \t', titles[i])
                        print('details : \t', newDetails)
                        print('further details : \t', newFurtherDetails)
                        print('backlinks : \t', newBacklinks)
                        fhand = open('zips.txt', 'a')
                        newcode = f"{zipcode} \n"
                        fhand.write(newcode)
                        fhand.close()
                    except:
                        pass
                driver.quit()
            except:
                pass
            break
        break



time.sleep(12000)
# rent = "Kaufen" # //*[@id="divSearchWhatFlyout"]/div[1]/ul/li[1]
# sale = "mieten"
# zipcode = "04289"
# subject = "wohnungen"
# page = requests.get(f"https://www.immowelt.de/liste/leipzig-meusdorf/{subject}/{rent}?geoid=10814365000032&sort=relevanz&zip={zipcode}")
# soup = BeautifulSoup(page.content, "html.parser")
# # print(soup)
# title = soup.findAll('h2')
# print(title)
# print(len(title))

