import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from modules import proxy
from rich.console import Console


options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
#options.add_argument('--headless')
#options.add_argument('--enable-gpu')
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

def source(URL=None, PROXY = None, user_agent=None):
    driver.delete_all_cookies()
    driver.delete_network_conditions()

    if re.findall(r'title', str(driver.page_source.title)):
        driver.delete_all_cookies()
        driver.delete_network_conditions()
        
        _proxy = proxy.create_proxy()
        options.add_argument('--proxy-server=%s' % _proxy)
        time.sleep(5)
    driver.get(URL)

    return driver.page_source