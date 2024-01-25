import os

from plyer import notification
import time
from selenium import webdriver
import pywhatkit
import pyautogui as pt
import keyboard
import cv2
# send the email
import smtplib

# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime

cwd = os.getcwd()
path = cwd + '/chromedriver.exe'
os.environ['PATH'] += path

while True:
    data1 = " "
    data2 = ' '
    driver = [1, 2, 3, 4, 5]
    name = ' '

    for i in range(1, 4):
        try:
            driver[i] = webdriver.Chrome()
            driver[i].get("https://ais.usvisa-info.com/en-tr/iv/users/sign_in")

            email_input = driver[i].find_element_by_id('user_email')
            email_input.send_keys('abdirahmaaan025@gmail.com')
            password_input = driver[i].find_element_by_id('user_password')
            password_input.send_keys('Mahad-025')
            check_box = driver[i].find_element_by_css_selector('label[for="policy_confirmed"]')
            check_box.click()
            sign_in_button = driver[i].find_element_by_name('commit')
            sign_in_button.click()

            url = driver[i].current_url

            continue_button = driver[i].find_element_by_xpath(
                "//*[@id='main']/div[2]/div[3]/div[1]/div/div[{}]/div[1]/div[2]/ul/li/a".format(i))
            continue_button.click()  # //*[@id="main"]/div[2]/div[3]/div[1]/div/div[{}]/div[1]/div[2]/ul/li/a
            name = driver[i].find_element_by_xpath('//*[@id="main"]/div[2]/div[1]/div/div/div')
            name = name.text
            url2 = driver[i].current_url

            schedule_appointment = driver[i].find_elements_by_class_name('accordion-item')
            schedule_appointment[0].click()

            new = driver[i].current_url.split('/')
            new.pop(-1)
            a = '/'
            new = a.join(new)
            new += '/continue'
            driver[i].get(new)

            driver[i].implicitly_wait(10)
            time.sleep(2)
            text = driver[i].find_element_by_xpath(
                '/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[1]/div[2]/small')
            print(name)
            print(text)
            print(i, text.text)
            data1 = str(text.text)
            print()

            if data1 != 'There are no available appointments at the selected location. Please try again later.':
                break

            time.sleep(2)

            driver[i].quit()
            time.sleep(2)
        except:
            time.sleep(0.01)
            driver[i].quit()

    if data1 != 'There are no available appointments at the selected location. Please try again later.':
        message = "For {}, \n go and check the website,\nThe appointment is available now\n\nMesssage written there is:\n {}".format(
            name, data1)

        try:
            pywhatkit.sendwhatmsg_instantly('+905523267748', message)
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
            TO = 'salmanmahad34@gmail.com'  # "Your To Email Ids " Can be a list
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

        time.sleep(720)

    time.sleep(120)






