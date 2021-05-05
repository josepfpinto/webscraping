import bin.config as Config
import google_sheets as Gsheets
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
import datetime as Date
import pandas as PD
from pandas.tseries.offsets import BusinessDay


# --- Initiates driver ---
def init_driver():
    print ('Init driver -------------')

    b = FirefoxBinary('/usr/bin/firefox')
    b.add_command_line_options("-private")

    driver = webdriver.Firefox(firefox_binary=b)
    driver.wait = WebDriverWait(driver, 2)

    return driver


# --- Set URL ---
def newURL (dateIn, totalDays, totalAdults):
    print ('newURL')

    try:
        day = str(dateIn.day)
        month = str(dateIn.month)
        year = str(dateIn.year)
        end_day = str(dateIn.day + totalDays)

        midURL = Config.midURL.format(month, day, year, month, end_day, year, totalAdults)
        url = Config.startURL + midURL + Config.endURL

        driver.get(url)

        w = WebDriverWait(driver, 8)
        w.until(expected_conditions.presence_of_element_located((By.TAG_NAME, "h1")))

    except TimeoutException:
        print("Timeout - no page load")

    except:
        print("URL FAILED!")


# --- Main Program ---    
if __name__ == "__main__":

    day = Date.datetime.today().strftime('%d-%m-%Y')

    # Initiate Google Sheets
    wks, wksInput = Gsheets.init(day)

    # Initiate browser & today date
    driver = init_driver()

    # Get User Data
    dateIn = Date.datetime.strptime(wksInput.acell('H5').value, '%d-%m-%Y').date()
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
        newURL (dateIn, totalDays, totalAdults)
        
        loopPages (day, dateIn, totalDays, cleaningFee, totalAdults)

        if i%2 == 0:
            dateOut = dateIn + BusinessDay(20)
        else:
            dateOut = dateIn + BusinessDay(25)
        dateIn = dateOut.date()
        
        i += 1
    
    # Close browser & close program 
    time.sleep(5)
    driver.quit()