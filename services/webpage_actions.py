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
        wait(15, "div._814193827")
    except (NoSuchElementException, TimeoutException) as error:
        exceptions.simple("- no apartments found: ", error)
        return error


def next_page(navBar):
    try:
        g_driver.google_driver.find_element(By.CSS_SELECTOR, navBar).find_element(By.CSS_SELECTOR,
                                                                                  "div.ce83a38554._ea2496c5b > button").click()
        wait(15, navBar)
    except (NoSuchElementException, TimeoutException) as error:
        exceptions.simple("- no next page button: ", error)
        return error


def get_price(apartment, totalAdults, totalDays, cleaningFee):
    text = apartment.find_element(By.CSS_SELECTOR, '[data-testid = "price-and-discounted-price"]').find_element(
        By.CLASS_NAME, 'fde444d7ef._e885fdc12').text
    priceText = text.split(' ')[-1]
    price = int(priceText.replace(',', ''))
    dayTax = int(totalAdults) * 2
    tax = 7 * dayTax if totalDays > 7 else totalDays * dayTax
    return (price - cleaningFee - tax) / totalDays


def get_score(apartment):
    scoreRaw = apartment.find_element(By.CLASS_NAME, '_9c5f726ff.bd528f9ea6').text
    return int(scoreRaw) if scoreRaw == "10" else float(scoreRaw[0] + "." + scoreRaw[2])


def get_reviews(apartment):
    reviewsRaw = apartment.find_element(By.CLASS_NAME, '_4abc4c3d5._1e6021d2f._6e869d6e0').text.split(' ')[0]
    return int(reviewsRaw[0] + reviewsRaw[2:] if (("," in reviewsRaw) or ("." in reviewsRaw)) else reviewsRaw)
