import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')


def source(URL="https://api.akakce.com/", proxy = None, user_agent=None):
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get("https://api.akakce.com/")
    time.sleep(15)
    return driver.page_source