# BOOKING.COM

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
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import pandas as pd
from pandas.tseries.offsets import BDay

# --- Initiates driver ---
def init_driver():
    print ('init_driver')
    b = firefox_binary=FirefoxBinary('C:\\\\Program Files\\\\Mozilla Firefox\\\\firefox.exe')
    b.add_command_line_options("-private")
    driver = webdriver.Firefox(firefox_binary=b)
    driver.wait = WebDriverWait(driver, 10)
    return driver


# --- Copies values from Booking.com ---
def copyValuesB (today, aptoList, dateR, tDays, cleaning, adults):
    try:
        platform = "B"
        for aptoItem in driver.find_elements_by_css_selector("div.sr_item.sr_item_new.sr_item_default.sr_property_block.sr_flex_layout"):
            availability = aptoItem.find_element_by_css_selector("div.sr_item_main_block div.sr-hotel__title-wrap h3.sr-hotel__title a.hotel_name_link.url span.invisible_spoken").text
            if (availability != "This property is unavailable on our site for your dates" and availability != "Este alojamiento no tiene disponibilidad en nuestra página en las fechas que has elegido"):
                name = aptoItem.find_element_by_css_selector("span.sr-hotel__name").text
                reviewsRaw = aptoItem.find_element_by_css_selector("div.bui-review-score__text").text
                z = reviewsRaw.index(" ")
                if ("," in reviewsRaw[:z]) or ("." in reviewsRaw[:z]):
                    reviews = int(reviewsRaw[0] + reviewsRaw[2:z])
                else:
                    reviews = int(reviewsRaw[:z])
                scoreRaw = aptoItem.find_element_by_css_selector("div.bui-review-score__badge")
                if scoreRaw.text == '10':
                    score = int (scoreRaw.text)
                else:
                    score = float(scoreRaw.text[0] + "." + scoreRaw.text[2])
                price = ""  
                for x in aptoItem.find_elements_by_css_selector("span.bui-u-sr-only"):
                    if ("Price" in x.text) or ("Precio" in x.text):
                        y = x.text.index("€") + 2
                        if ("," in x.text[y:]) or ("." in x.text[y:]):
                            zlen = 0
                            if "," in x.text[y:]:
                                zlen = x.text.index(",") - x.text.index("€")
                            if "." in x.text[y:]:
                                zlen = x.text.index(".") - x.text.index("€")
                            if zlen > 3:
                                z = y + 3
                                price = int(int(x.text[y] + x.text[y+1] + x.text[z:]))                            
                            else:
                                z = y + 2
                                price = int(int(x.text[y] + x.text[z:]))
                        else:
                            price = int(int(x.text[y:]))
                if tDays > 7:    
                    tax = 7*int(adults)*2
                else:
                    tax = tDays*int(adults)*2 
                price = (price - cleaning - tax) / tDays
                aptoList.append([platform, today, dateR, name, reviews, score, price]) 
    except TimeoutException:
        print("Copy Values FAILED!")

            
# --- Sends values to sheet ---
def sendValues (finalList):
    print ('sendValues')
    try: 
        emptyCell = len(wks.col_values(1))+1
        sh.values_update(
        'Sheet1!A{}'.format(emptyCell), 
        params={"valueInputOption": "RAW"}, 
        body={"values": finalList}
        )
    except TimeoutException:
        print("Sending values to GSheet FAILED!")


# --- Pages loop ---
def loopPages (thisday, dateReservation, totalD, cleaningF, tAdults):
    print ('loopPages')
    try: 
        time.sleep(15)
        try: 
            cookiesButton = driver.find_element_by_css_selector("button.cookie-warning-v2__banner-cta").click()
            time.sleep(3)
        except NoSuchElementException:
            time.sleep(1)
        dateReserv = dateReservation.strftime('%d-%m-%Y')
        sheetList = []
        pages = driver.find_elements_by_css_selector("li.bui-pagination__item") 
        numPages = len(pages)-2
        for page in range(numPages):
            print ("-- Page: ", page)
            copyValuesB (thisday, sheetList, dateReserv, totalD, cleaningF, tAdults)
            print ("Length: ", len(sheetList))
            nextButton = driver.find_element_by_css_selector(".bui-pagination__next-arrow").click()
            time.sleep(15)
        sendValues(sheetList)
    except TimeoutException:
        print("Pages loop FAILED!")
    
    
# --- Get New URL ---
def newURL (newDate, newIntro, newEnd, days, adults):
    print ('newURL')
    try:
        dI = str(newDate.day)
        mI = str(newDate.month)
        yI = str(newDate.year)
        dO = str(newDate.day + days)
        mO = str(newDate.month)
        yO = str(newDate.year)
        dateURL = "checkin_month={}&checkin_monthday={}&checkin_year={}&checkout_month={}&checkout_monthday={}&checkout_year={}&city=-2173088&class_interval=1&dest_id=-2173088&dest_type=city&from_sf=1&group_adults={}".format(mI, dI, yI, mO, dO, yO, adults)
        urlInput = newIntro + dateURL + newEnd
        driver.get(urlInput)
    except TimeoutException:
        print("URL FAILED!")
    
    
# --- Main Program ---    
if __name__ == '__main__':
    
    #Google API
    scope = ["https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name('pythonPriceCheck-7aa1e04e69ac_DriveAPI.json', scope)
    goog = gspread.authorize(credentials)
    sh = goog.open('Analise Concorrencia')
    wks = goog.open('Analise Concorrencia').sheet1
    wksInput = sh.get_worksheet(1)
    
    #Initiate Browser & Today Date
    driver = init_driver()
    day = datetime.datetime.today().strftime('%d-%m-%Y')
    
    # ---User Data---
    #coinURL = "&selected_currency=EUR&changed_currency=1&top_currency=1"
    introURL = "https://www.booking.com/searchresults.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaDKIAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4ApTC-esFwAIB&sid=c3d69b959fae02738bb57461413ede72&tmpl=searchresults&"
    endURL = "&group_children=0&label_click=undef&nflt=ht_id%3D201%3Breview_score%3D80%3Bdistance%3D1000%3Bhotelfacility%3D107%3Broomfacility%3D38%3Bdi%3D1279%3Bmin_bathrooms%3D1%3B&no_rooms=2&offset=0&percent_htype_apt=1&raw_dest_type=city&room1=A&room2=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=1&src=searchresults&srpvid=1d28860b68600070&ss=Porto&ssb=empty&ssne=Porto&ssne_untouched=Porto&top_ufis=1&selected_currency=EUR&changed_currency=1&top_currency=1"
    #dateIn = datetime.date(2020,2,17)
    #months = 5
    dateIn = datetime.datetime.strptime(wksInput.acell('H5').value, '%d-%m-%Y').date()
    months = int(wksInput.acell('I5').value)
    totalDays = int(wksInput.acell('K5').value)
    totalAdults = str(wksInput.acell('L5').value)
    cleaningFee = int(wksInput.acell('M5').value)
    
    # Clean or not to clean
    if len(wks.row_values(2)) > 1 and wks.row_values(2)[1] == day:
        print ("SAME DAY!")
    else:
        wks.clear()
        wks.append_row(["PLATF", "TODAY", "DATE", "NAME", "RESERVAS", "SCORE", "PRICES", "SUPERHOST"]) 
    
    #Find and Copy Values to Sheet
    print ('START!')
    i = 0
    while i < months:
        print ("---- ", dateIn, " ----")
        time.sleep(5)
        newURL (dateIn, introURL, endURL, totalDays, totalAdults)
        loopPages (day, dateIn, totalDays, cleaningFee, totalAdults)
        if i%2 == 0:
            dateOut = dateIn + BDay(20)
        else:
            dateOut = dateIn + BDay(25)
        dateIn = dateOut.date()
        i += 1
    
    time.sleep(5)
    driver.quit()
