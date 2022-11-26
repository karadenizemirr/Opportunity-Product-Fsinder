import requests
from bs4 import BeautifulSoup

session = requests.Session()

base_url ="https://www.akakce.com"

s_req = session.get(base_url)
html = BeautifulSoup(s_req.text, 'html.parser').findAll("form")

action = html[0]['action']

md = html[0].findAll('input', {'name': 'md'})
r = html[0].findALl('input', {'name': 'r'})

print(md)
print(r)