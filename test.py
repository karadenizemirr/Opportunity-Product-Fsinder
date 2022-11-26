import requests
from bs4 import BeautifulSoup

URL = "https://www.akakce.com"
session = requests.Session()

req = session.get(URL)
html = BeautifulSoup(req.text, "html.parser")

action = html.findAll("form")[0]['action']
md = html.findAll("input", {'name': 'md'})
print(md)