import google_sheets as Gsheets
import time
from selenium.common.exceptions import TimeoutException

import main
from services import webpage_actions, exceptions

is_first_page = True
driver = main.driver


# --- Loops through all available pages with apartments within the search parameters ---
def loop_pages(day, dateIn, totalDays, cleaningFee, totalAdults):
    print("\nLooping pages")
    global is_first_page

    try:
        if is_first_page:  # Click in cookies button
            webpage_actions.close_cookies()

        dateIn = dateIn.strftime("%d-%m-%Y")
        sheetList = []

        # Loop through pages
        pages = int(
            driver.find_element_by_css_selector("li.bui-pagination__item:nth-child(7) > a:nth-child(1) > "
                                                "div:nth-child(2)").text)

        for page in range(pages):
            time.sleep(2)
            print("- page: ", page)
            scrape_page(day, sheetList, dateIn, totalDays, cleaningFee, totalAdults)
            print("- length of apartment list for page ", page, ": ", len(sheetList))

            if page != pages - 1:
                driver.find_element_by_css_selector(".paging-next").click()
                webpage_actions.wait(15, "ul.bui-pagination__list")

        Gsheets.send_values(sheetList)

    except TimeoutException as error:
        exceptions.simple("Timeout - failed to loop pages. Error:", error)

    except Exception as error:
        exceptions.more_info("Pages loop FAILED!", error)


# --- Copies values from Booking.com ---
def scrape_page(day, sheetList, dateIn, totalDays, cleaningFee, totalAdults):
    print("\nScraping page")

    try:
        platform = "B"
        webpage_actions.wait_for_apartments()
        apartmentList = driver.find_elements_by_css_selector(
            "div.sr_item.sr_item_new.sr_item_default.sr_property_block.sr_flex_layout")

        # Getting info for each apartment
        for apartment in apartmentList:
            name = apartment.find_element_by_css_selector("span.sr-hotel__name").text
            reviews = webpage_actions.get_reviews(apartment)
            score = webpage_actions.get_score(apartment)
            price = webpage_actions.get_price(apartment, totalAdults, totalDays, cleaningFee)
            sheetList.append([platform, day, dateIn, name, reviews, score, price])

    except TimeoutException as error:
        exceptions.simple("Timeout - failed to scrape page. Error:", error)

    except Exception as error:
        exceptions.more_info("Scrape page FAILED!", error)
