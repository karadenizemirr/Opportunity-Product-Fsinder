import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path = None

if os.name == 'nt':
    path = "modules/bypass/chromedriver.exe"
else:
    path = "modules/bypass/chromedriver"

chrome_option = Options()

driver = webdriver.Chrome(path, chrome_options=chrome_option)

def create_bypass(link):
    driver.get(link)
    