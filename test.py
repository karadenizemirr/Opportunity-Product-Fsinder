import requests
from bs4 import BeautifulSoup

session = requests.Session()

base_url ="https://www.akakce.com"

s_req = session.get(base_url)
html = BeautifulSoup(s_req.text, 'html.parser').findAll("form")