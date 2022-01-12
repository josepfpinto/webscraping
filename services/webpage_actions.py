import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from services import exceptions, webpage_scraping, g_driver


def wait(seconds, css_selector):
    w = WebDriverWait(g_driver.google_driver, seconds)
    if len(css_selector) > 1:
        w.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, css_selector)))


def close_cookies():
    print("- closing cookies")
    try:
        w = WebDriverWait(g_driver.google_driver, 15)
        w.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button#onetrust-accept-btn-handler")))
        g_driver.google_driver.find_element_by_css_selector(
            "button#onetrust-accept-btn-handler").click()
        print("- cookie button clicked")
    except (NoSuchElementException, TimeoutException) as error:
        exceptions.simple("- no cookie button found... Moving on:", error)

    finally:
        webpage_scraping.is_first_page = False
        time.sleep(3)


def wait_for_apartments():
    try:
        wait(15, "div.sr_item.sr_item_new.sr_item_default.sr_property_block.sr_flex_layout")
    except (NoSuchElementException, TimeoutException) as error:
        exceptions.simple("- no apartments found:", error)
        return error


def get_price(apartment, totalAdults, totalDays, cleaningFee):
    price = ""
    for elem in apartment.find_elements_by_css_selector("span.bui-u-sr-only"):
        text = elem.text
        if ("Price" in text) or ("Preço" in text):
            price = int(text.split(' ')[-1])
    dayTax = int(totalAdults) * 2
    tax = 7 * dayTax if totalDays > 7 else totalDays * dayTax
    return (price - cleaningFee - tax) / totalDays


def get_score(apartment):
    scoreRaw = apartment.find_element_by_css_selector(
        "div.bui-review-score__badge").text
    return int(scoreRaw) if scoreRaw == "10" else float(scoreRaw[0] + "." + scoreRaw[2])


def get_reviews(apartment):
    reviewsRaw = apartment.find_element_by_css_selector(
        "div.bui-review-score__text").text.split(' ')[0]
    return int(reviewsRaw[0] + reviewsRaw[2:] if (("," in reviewsRaw) or ("." in reviewsRaw)) else reviewsRaw)
