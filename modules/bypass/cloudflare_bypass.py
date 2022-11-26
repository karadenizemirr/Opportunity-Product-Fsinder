import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

service = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def create_bypass(URL):
    driver.get(URL)
    time.sleep(3600)