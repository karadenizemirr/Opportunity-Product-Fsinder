import requests
from bs4 import BeautifulSoup

URL = "https://www.akakce.com"
session = requests.Session()

req = session.get(URL)
html = BeautifulSoup(req.text, "html.parser")

md = html.findAll("input", {"name": "md"})
r = html.findAll("input", {"name": "r"})


print(r)