import requests
from bs4 import BeautifulSoup

URL = "https://www.akakce.com"
session = requests.Session()

req = session.get(URL)
print(req.text)