import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path = None

if os.name == 'nt':
    path = "modules/bypass/chromedriver.exe"
else:
    path = "modules/bypass/chromedriver"


driver = webdriver.Chrome(path)
