import config.driver as driverPath
from selenium import webdriver
import time

from services import webpage_actions

google_driver = webdriver.Chrome


def init():
    global google_driver

    print("\nInit driver")
    chromeDriver = webdriver.Chrome(driverPath.path)
    webpage_actions.wait(10, "")
    google_driver = chromeDriver


def close():
    time.sleep(5)
    google_driver.quit()
