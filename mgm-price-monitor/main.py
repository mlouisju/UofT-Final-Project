import schedule
import time
import sys
import os
import platform

from bs4 import BeautifulSoup
from money_parser import price_str

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

# Importing the editable variables/settings
import settings



def login(browser):
    wait = WebDriverWait(browser, 10);
    
    print("Attempting to Login...")
    browser.maximize_window()
    
    # Navigate to Sign In page
    browser.get('https://excalibur.mgmresorts.com/en/sign-in.html')
    
    # Wait for page to load (until we see the input box for sign in email)
    wait.until(EC.presence_of_element_located((By.ID, 'sign-in-email')))
    
    # Type in the email/password
    browser.find_element_by_id('sign-in-email').send_keys(settings.MGM_EMAIL)
    browser.find_element_by_id("sign-in-password").send_keys(settings.MGM_PASSWORD)
    
    # find and click the sign in button
    sign_in_button = browser.find_element_by_id("sign-in")
    sign_in_button.click();
    
    # Wait for next page to load (hang tight until we see an element on the account page, after successful login)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "acc-sum-welcome__guest")))
    print("Logged In!")





def searchAndParse(browser):
    wait = WebDriverWait(browser, 10);
    
    browser.get("https://excalibur.mgmresorts.com/en/booking/room-booking.html#/rooms?po=0&numGuests=2&arrive=2019-05-15&depart=2019-05-21")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "room-list-wrapper")))
    
    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
    print("=================")
    print("Currently Available Rooms:")

    for roomContainer in soup.select("div.room-list-wrapper"):
        # Get the room's full name
        title = roomContainer.select("h3.room-title")[0].text
        
        # Find and delete the striked out prices (old price vs sale price)
        strikedPrices = roomContainer.select("span.room-offer-price.strike")
        for match in strikedPrices:
            match.decompose()
            
        # Get the remaining price (without a strike through it)
        price = price_str(roomContainer.select("span.room-offer-price")[0].text)
        
        print(title, price)
        
        # Check if room title matches any of the booked room titles
        for bookedRoom in settings.bookedRoomList:
            if bookedRoom['title'] == title:
                # Found a match! Let's compare prices and send email if it's cheaper, otherwise do nothing
                priceDifference = float(bookedRoom['price']) - float(price)
                if priceDifference > 0:
                    sendEmail(title, price, priceDifference)
        
        
        


def sendEmail(title, price, priceDifference):
    print("Sending Email...")
    
    # Copied and pasted snippet from the library's docs: https://github.com/sendgrid/sendgrid-python
    message = Mail(
        from_email=settings.EMAIL_TO,
        to_emails=settings.EMAIL_TO,
        subject='Found a lower room price!',
        html_content=f"{title} is now ${price}. <br/> Total Savings: ${priceDifference}"
    )
        
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print("Email Sent!")
    except Exception as e:
        print(e)
    
    



def main():
    # Path to the Chrome app for MacOS
    driverPath = os.getcwd()+"/drivers/mac/chromedriver";
    
    # Launch a fresh/new chrome browser window
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(chrome_options=options, executable_path=driverPath)
    
    # Time for the magic to happen...
    login(browser)
    searchAndParse(browser)
    
    # Close the browser window (even if invisible)
    browser.close()
    
    print("Done! Waiting for next run...")


# Run Script once when we run the actual python script for the first time
main()

# Then schedule the script to run on a set interval
schedule.every(30).minutes.do(main)
while True:
	schedule.run_pending()
	time.sleep(1)
