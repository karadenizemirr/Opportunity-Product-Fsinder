import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)



def create_session(URL="https://api.akakce.com/"):
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get("https://api.akakce.com/")
    print(driver.page_source)


create_session()