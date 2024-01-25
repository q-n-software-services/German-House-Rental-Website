from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from plyer import notification
import time
from ipware import get_client_ip
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
from django.utils import timezone
import pywhatkit
import pyautogui as pt
import keyboard
from .models import listings, subscriptions
import cv2
# send the email
import smtplib
import os
import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()

options.headless = True

# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime

# Create your views here.


def homepage(request):
    this_ip = get_client_ip(request)[0]
    print("this is the IP = ", this_ip)
    return render(request, 'index.html', {"available": "True"})


def RealEstate(request):
    # sendMessages("Hi Muhammad Mohib. This is your first automated website")
    return render(request, 'realestate.html')



def website1(request):
    cwd = os.getcwd()
    path = cwd + '/chromedriver.exe'
    os.environ['PATH'] += path
    zips = open("zips.txt", 'r')
    zips = zips.readlines()
    zipcodes = ''
    for item in zips:
        zipcodes += "," + item.strip()
    zipcodes = zipcodes.split(",")

    for i, item in enumerate(zipcodes):
        if len(item.strip()) != 5:
            zipcodes.pop(i)
        else:
            zipcodes[i] = item.strip()

    print(zipcodes)
    print(len(zipcodes))
    for zipcode in zipcodes:
        for x in range(1, 3):
            for y in range(1, 10):
                try:
                    print(zipcode)
                    print(x, y)
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
                                "location":
                                    str(furtherDetails[2 * i]).split('location</i><span>')[1].strip().split("<")[
                                        0].strip(),
                                "check":
                                    str(furtherDetails[(2 * i) + 1]).split('check</i><span>')[1].strip().split("<")[
                                        0].strip()}

                            newBacklinks = {
                                "link": str(backLinks[i]).split('<a class="mainSection-b22fb noProject-eaed4" href="')[
                                    1].strip().split('"')[0].strip(),
                                "image":
                                    str(backLinks[i]).split('<picture><source data-srcset="')[1].strip().split('"')[
                                        0].strip()}

                            print('title : \t', titles[i])
                            print('details : \t', newDetails)
                            print('further details : \t', newFurtherDetails)
                            print('backlinks : \t', newBacklinks)
                            if x == 1:
                                category = 'Rent'
                                if y == 1:
                                    SubCategory = 'apartment'
                                elif y == 2:
                                    SubCategory = 'a house'
                                elif y == 3:
                                    SubCategory = 'temporary living'
                                elif y == 4:
                                    SubCategory = 'Shared apartment'
                                elif y == 5:
                                    SubCategory = 'commercial real estate'
                                elif y == 6:
                                    SubCategory = 'garage/parking space'
                                elif y == 7:
                                    SubCategory = 'property'
                                elif y == 8:
                                    SubCategory = 'new construction project'
                                elif y == 9:
                                    SubCategory = 'Miscellaneous'
                            elif x == 2:
                                category = "Buy"
                                if y == 1:
                                    SubCategory = 'a house'
                                elif y == 2:
                                    SubCategory = 'apartment'
                                elif y == 3:
                                    SubCategory = 'new construction project'
                                elif y == 4:
                                    SubCategory = 'commercial real estate'
                                elif y == 5:
                                    SubCategory = 'property'
                                elif y == 6:
                                    SubCategory = "income property"
                                elif y == 7:
                                    SubCategory = 'garage'
                                elif y == 8:
                                    SubCategory = 'type house'
                                elif y == 9:
                                    SubCategory = 'Miscellaneous'
                            else:
                                category = "NONE"
                                SubCategory = "NONE"

                            currentdate = timezone.now()
                            created_obj = listings.objects.create(added_date=currentdate, heading=titles[i],
                                                                  price=newDetails['price'],
                                                                  area=newDetails['area'], rooms=newDetails['rooms'],
                                                                  location=newFurtherDetails['location'],
                                                                  check12=newFurtherDetails['check'],
                                                                  link=newBacklinks["link"],
                                                                  image=newBacklinks["image"],
                                                                  zipcode=zipcode, category=category,
                                                                  SubCategory=SubCategory)

                        except:
                            pass
                    driver.quit()
                except:
                    pass
    return render(request, "<h1>ALL DONE !!!</h1>")


@csrf_exempt
def subscribe(request):
    currentdate = timezone.now()
    content = request.POST["email"]
    WAnumber = request.POST["number"]
    name = request.POST["name"]
    this_ip = get_client_ip(request)[0]
    created_obj = subscriptions.objects.create(added_date=currentdate, name=name, WAnumber=WAnumber, ip=this_ip, email=content)
    return HttpResponseRedirect('/')


def sendMessages(message):
    try:
        pywhatkit.sendwhatmsg_instantly('+923131521624', message)
        position = pt.locateOnScreen('send_button12.png', confidence=0.9)
        pt.moveTo(position)
        pt.click()
        time.sleep(2)
        keyboard.press_and_release('ctrl+w')
        keyboard.press('space')
    except:
        time.sleep(0.01)

    try:
        now = datetime.datetime.now()
        # email content placeholder
        content = ''
        cnt = "<h1><pre>{}</pre></h1>".format(message)
        content += cnt
        content += ('<br>------<br>')
        content += ('<br><br>End of Message')

        # Update your Email Details

        SERVER = 'smtp-relay.sendinblue.com'  # your smtp server
        PORT = 587  # your Port Number
        FROM = 'qnsoftwareservices12272@gmail.com'  # "Your From Email ID"
        TO = 'muhammadmohib3@gmail.com'  # "Your To Email Ids " Can be a list
        PASS = '5Yq9UA7dWMCGLx3v'  # "Your Email Id's Password

        # Create a text/plain message
        msg = MIMEMultipart()
        msg.add_header('Content-Disposition', 'attachment', filename='HongKong project.py')
        msg['Subject'] = 'UPDATE :\t\t' + '' + str(now.day) + '-' + str(now.month) + '-' + str(
            now.year) + '\ttime :\t\t' + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
        msg['From'] = FROM
        msg['To'] = TO
        msg.attach(MIMEText(content, 'html'))

        print("Initializing Server....")
        server = smtplib.SMTP(SERVER, PORT)
        server.set_debuglevel(0)
        server.ehlo()
        server.starttls()
        server.login(FROM, PASS)
        server.sendmail(FROM, TO, msg.as_string())

        print('Email Sent !')
        server.quit()
    except:
        time.sleep(0.01)

    try:
        notification.notify(
            title="\t\tUPDATE",
            message=message,
            timeout=12
        )
    except:
        time.sleep(0.01)


def travel(request):
    return render(request, 'travel.html')


def vehicles(request):
    return render(request, 'vehicles.html')


def shopping(request):
    return render(request, 'shopping.html')
