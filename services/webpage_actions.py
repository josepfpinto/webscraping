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
        g_driver.google_driver.find_element(By.CSS_SELECTOR,
                                            "button#onetrust-accept-btn-handler").click()
        print("- cookie button clicked")
    except (NoSuchElementException, TimeoutException) as error:
        exceptions.simple("- no cookie button found... Moving on: ", error)

    finally:
        webpage_scraping.is_first_page = False
        time.sleep(3)


def wait_for_apartments():
    try:
        wait(15, "div.a826ba81c4.fe821aea6c.fa2f36ad22.afd256fc79.d08f526e0d.ed11e24d01.da89aeb942")
    except (NoSuchElementException, TimeoutException) as error:
        exceptions.simple("- no apartments found: ", error)
        return error


def next_page():
    try:
        g_driver.google_driver.find_element(By.CSS_SELECTOR,'[aria-label="Next page"]').click()
        wait_for_apartments()
    except (NoSuchElementException, TimeoutException) as error:
        exceptions.simple("- no next page button: ", error)
        return error


def get_price(apartment, totalAdults, totalDays, cleaningFee):
    text = apartment.find_element(By.CSS_SELECTOR, '[data-testid = "price-and-discounted-price"]').find_element(
        By.CLASS_NAME, 'fcab3ed991.bd73d13072').text
    priceText = text.split(' ')[-1]
    price = float(priceText.replace(',', ''))
    dayTax = int(totalAdults) * 2
    tax = 7 * dayTax if totalDays > 7 else totalDays * dayTax
    return round((price - cleaningFee - tax) / totalDays)


def get_score(apartment):
    try:
        scoreRaw = apartment.find_element(By.CLASS_NAME, 'b5cd09854e.d10a6220b4').text
    except NoSuchElementException:
        try:
            scoreRaw = apartment.find_element(By.CLASS_NAME, 'b5cd09854e.f0d4d6a2f5.e46e88563a').text
            scoreRaw = scoreRaw.split(' ')[-1]
        except Exception:
            scoreRaw = '0'
    return int(scoreRaw) if scoreRaw == "10" else float(scoreRaw[0] + "." + scoreRaw[2])


def get_reviews(apartment):
    try:
        reviewsRaw = apartment.find_element(By.CLASS_NAME, 'd8eab2cf7f.c90c0a70d3.db63693c62').text
        reviewsRaw = reviewsRaw.split(' ')[0]
    except NoSuchElementException:
        reviewsRaw = '0'
    return int(reviewsRaw[0] + reviewsRaw[2:] if (("," in reviewsRaw) or ("." in reviewsRaw)) else reviewsRaw)
