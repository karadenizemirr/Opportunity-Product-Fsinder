import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


chrome_option = Options()
service=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, chrome_options=chrome_option)

def create_bypass(link):
    driver.get(link)
    time.sleep(3600)