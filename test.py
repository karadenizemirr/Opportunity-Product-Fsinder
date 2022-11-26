import requests
from bs4 import BeautifulSoup

session = requests.Session()

base_url ="https://www.akakce.com"

s_req = session.get(base_url)
html = BeautifulSoup(s_req.text, 'html.parser').findAll("form")[0]

action = html['action']

md = html.findAll('input', {'name': 'md'})
r = html.findALl('input', {'name': 'r'})

print(md)
print(r)