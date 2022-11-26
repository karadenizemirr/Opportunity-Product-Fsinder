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
#options.add_argument('--disable-gpu')
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

def source(URL=None, proxy = None, user_agent=None):
    driver.delete_all_cookies()
    driver.get(URL)

    if re.findall(r'403|Forbidden|Access|denied', str(driver.page_source)):
        driver.delete_all_cookies()
        _proxy = proxy.create_proxy()
        options.add_argument("--proxy-server=%s" % _proxy)
        time.sleep(5)

    return driver.page_source