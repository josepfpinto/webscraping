import bin.config as config
import googleSheets
import time
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import datetime
import pandas as pd
from pandas.tseries.offsets import BDay


# --- Initiates driver ---
def init_driver():
    print ('Init driver -------------')
    b = FirefoxBinary('/usr/bin/firefox')
    b.add_command_line_options("-private")
    driver = webdriver.Firefox(firefox_binary=b)
    driver.wait = WebDriverWait(driver, 5)
    return driver



# --- Main Program ---    
if __name__ == "__main__":

    # Initiate Google Sheets
    wks, wksInput = googleSheets.init()

    # Initiate browser & today date
    driver = init_driver()
    day = datetime.datetime.today().strftime('%d-%m-%Y')

    time.sleep(2)

    # Get User Data
    dateIn = datetime.datetime.strptime(wksInput.acell('H5').value, '%d-%m-%Y').date()
    months = int(wksInput.acell('I5').value)
    totalDays = int(wksInput.acell('K5').value)
    totalAdults = str(wksInput.acell('L5').value)
    cleaningFee = int(wksInput.acell('M5').value)

    #Find and Copy Values to Sheet
    print ('START!')

    i = 0
    while i < months:
        print ("---- ", dateIn, " ----")
        # time.sleep(5)
        newURL (dateIn, introURL, endURL, totalDays, totalAdults)
        loopPages (day, dateIn, totalDays, cleaningFee, totalAdults)
        if i%2 == 0:
            dateOut = dateIn + BDay(20)
        else:
            dateOut = dateIn + BDay(25)
        dateIn = dateOut.date()
        i += 1

    # Close browser & close program 
    time.sleep(5)
    driver.quit()