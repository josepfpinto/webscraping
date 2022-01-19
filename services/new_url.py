import config.web_url as webUrl
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from services import webpage_actions, exceptions, g_driver


def get(dateIn, totalDays, totalAdults, numberRooms):
    print("\nCreating and fetching new URL")

    try:
        startDay = str(dateIn.day)
        month = str(dateIn.month)
        year = str(dateIn.year)
        endDay = str(dateIn.day + totalDays)
        midURL = webUrl.mid.format(month, startDay, year, month, endDay, year, totalAdults, numberRooms)
        g_driver.google_driver.get(webUrl.start + midURL + webUrl.end)
        webpage_actions.wait(15, "div.sr_header")

    except (NoSuchElementException, TimeoutException) as error:
        exceptions.simple("Timeout - no page load. Error:", error)

    except Exception as error:
        exceptions.more_info("URL FAILED!", error)