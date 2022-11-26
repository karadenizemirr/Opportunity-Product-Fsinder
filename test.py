import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
driver.get("https://www.akakce.com/")
time.sleep(60)