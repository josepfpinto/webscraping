import google_sheets as Gsheets
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


# --- Loops through all available pages with apartments within the search parameters ---
def loop_pages (driver, day, dateIn, totalDays, cleaningFee, totalAdults):

    print ('\nLooping pages')

    try: 
        # Click in cookies button 
        try: 
            w = WebDriverWait(driver, 15)
            w.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button#onetrust-accept-btn-handler")))
            
            driver.find_element_by_css_selector("button#onetrust-accept-btn-handler").click()

        except (NoSuchElementException, TimeoutException) as error:
            print("No cookie button found... Moving on. Error: ", error)
            time.sleep(1)

        dateIn = dateIn.strftime('%d-%m-%Y')
        sheetList = []

        # Loop through pages
        pages = driver.find_elements_by_css_selector("ul.bui-pagination__list") 
        numPages = len(pages)-2

        for page in range(numPages):
            print ("- Page: ", page)

            # scrape_page (day, sheetList, dateIn, totalDays, cleaningFee, totalAdults)
            print ("Length of apartment list for page ", page, ": ", len(sheetList))

            nextButton = driver.find_element_by_css_selector(".bui-pagination__next-arrow").click()
            
            w = WebDriverWait(driver, 15)
            w.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.bui-pagination__list")))

        # Gsheets.send_values(sheetList)
    
    except TimeoutException as error:
        print("Timeout - failed to loop pages. Error: ", error)

    except Exception as error:
        print("Pages loop FAILED! Error: ", error)

"""
# --- Copies values from Booking.com ---
def scrape_page (today, aptoList, dateR, tDays, cleaning, adults):
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
"""