import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

from services import webpage_actions, exceptions, google_sheets as Gsheets, g_driver

is_first_page = True


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
        try:
            pages = int(
                g_driver.google_driver.find_element(By.CSS_SELECTOR,
                                                    "div.e603a69fe1 > ol._5312cbccb > li.ce83a38554:last-child > button").text)
        except NoSuchElementException:
            pages = 1

        print("pages: " + str(pages))

        for page in range(pages):
            time.sleep(2)
            print("- page: ", page)
            scrape_page(day, sheetList, dateIn, totalDays, cleaningFee, totalAdults)
            print("- length of apartment list for page ", page, ": ", len(sheetList))

            if 0 != pages - 1:
                webpage_actions.next_page("div._5312cbccb")

        Gsheets.send_values(sheetList)

    except TimeoutException as error:
        exceptions.simple("Timeout - failed to loop pages. Error: ", error)

    except Exception as error:
        exceptions.more_info("Pages loop FAILED!", error)


# --- Copies values from Booking.com ---
def scrape_page(day, sheetList, dateIn, totalDays, cleaningFee, totalAdults):
    print("\nScraping page")

    try:
        platform = "B"
        webpage_actions.wait_for_apartments()
        apartmentList = g_driver.google_driver.find_elements(By.CSS_SELECTOR, '[data-testid = "property-card"]')

        # Getting info for each apartment
        for apartment in apartmentList:
            name = apartment.find_element(By.CSS_SELECTOR, '[data-testid = "title"]').text
            reviews = webpage_actions.get_reviews(apartment)
            score = webpage_actions.get_score(apartment)
            price = webpage_actions.get_price(apartment, totalAdults, totalDays, cleaningFee)
            sheetList.append([platform, day, dateIn, totalAdults, name, reviews, score, price])

    except TimeoutException as error:
        exceptions.simple("Timeout - failed to scrape page. Error:", error)

    except Exception as error:
        exceptions.more_info("Scrape page FAILED!", error)
