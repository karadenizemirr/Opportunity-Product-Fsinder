import requests
from bs4 import BeautifulSoup

session = requests.Session()

base_url ="https://www.akakce.com"

s_req = session.get(base_url)
html = BeautifulSoup(s_req.text, 'html.parser').findAll("form")[0]

action = html['action']

all_input = html.findAll('input')

md = all_input[0]['value']
r = all_input[1]['value']

r_req = session.post(f"{base_url}/{action}", data = {
    "md": md,
    "r": r
})

print(r_req.text)