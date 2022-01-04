import config.driver as driverPath
from selenium import webdriver
import time

import main
from services import webpage_actions


def init():
    print("\nInit driver")
    chromeDriver = webdriver.Chrome(driverPath.path)
    webpage_actions.wait(10, "")
    main.driver = chromeDriver


def close():
    time.sleep(5)
    main.driver.quit()
