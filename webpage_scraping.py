import sys
import os
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


is_first_page = True


# --- Loops through all available pages with apartments within the search parameters ---
def loop_pages(driver, day, dateIn, totalDays, cleaningFee, totalAdults):

    print("\nLooping pages")
    global is_first_page

    try:
        if is_first_page:  # Click in cookies button
            try:
                w = WebDriverWait(driver, 15)
                w.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button#onetrust-accept-btn-handler")))

                driver.find_element_by_css_selector(
                    "button#onetrust-accept-btn-handler").click()

                is_first_page = False
                print("- cookie button clicked")

            except (NoSuchElementException, TimeoutException) as error:
                print("- no cookie button found... Moving on.")

            finally:
                time.sleep(3)

        dateIn = dateIn.strftime("%d-%m-%Y")
        sheetList = []

        # Loop through pages
        pages = int(
            driver.find_element_by_css_selector("li.bui-pagination__item:nth-child(7) > a:nth-child(1) > div:nth-child(2)").text)

        for page in range(pages):

            time.sleep(2)
            print("- page: ", page)

            scrape_page(driver, day, sheetList, dateIn,
                        totalDays, cleaningFee, totalAdults)
            print("- length of apartment list for page ",
                  page, ": ", len(sheetList))

            if page != pages - 1:
                nextButton = driver.find_element_by_css_selector(
                    ".paging-next").click()

                w = WebDriverWait(driver, 15)
                w.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "ul.bui-pagination__list")))

        Gsheets.send_values(sheetList)

    except TimeoutException as error:
        print("\nTimeout - failed to loop pages. Error: ", error)

    except Exception as error:
        print("\nError | Pages loop FAILED!")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, " ", error)


# --- Copies values from Booking.com ---
def scrape_page(driver, day, sheetList, dateIn, totalDays, cleaningFee, totalAdults):

    print("\nScraping page")

    try:
        platform = "B"

        try:
            w = WebDriverWait(driver, 15)

            # get apartment list
            w.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.sr_item.sr_item_new.sr_item_default.sr_property_block.sr_flex_layout")))

        except (NoSuchElementException, TimeoutException) as error:
            print("- no apartments found...")
            return null

        apartmentList = driver.find_elements_by_css_selector(
            "div.sr_item.sr_item_new.sr_item_default.sr_property_block.sr_flex_layout")

        # Getting info for each apartment
        for apartment in apartmentList:

            # name
            name = apartment.find_element_by_css_selector(
                "span.sr-hotel__name").text

            # reviews
            reviewsRaw = apartment.find_element_by_css_selector(
                "div.bui-review-score__text").text.split(' ')

            if ("," in reviewsRaw[0]) or ("." in reviewsRaw[0]):
                reviews = int(reviewsRaw[0][0] + reviewsRaw[0][2:])
            else:
                reviews = int(reviewsRaw[0])

            # score
            scoreRaw = apartment.find_element_by_css_selector(
                "div.bui-review-score__badge").text

            if scoreRaw == "10":
                score = int(scoreRaw)
            else:
                score = float(scoreRaw[0] + "." + scoreRaw[2])

            # price
            price = ""
            for elem in apartment.find_elements_by_css_selector("span.bui-u-sr-only"):

                text = elem.text
                if ("Price" in text) or ("Preço" in text):
                    price = int(text.split(' ')[-1])

            if totalDays > 7:
                tax = 7 * int(totalAdults) * 2
            else:
                tax = totalDays * int(totalAdults) * 2

            price = (price - cleaningFee - tax) / totalDays

            sheetList.append(
                [platform, day, dateIn, name, reviews, score, price])

    except TimeoutException as error:
        print("\nTimeout - failed to scrape page. Error: ", error)

    except Exception as error:
        print("\nError | Scrape page FAILED!")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, " ", error)
