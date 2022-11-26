import requests
from modules import bypass

session = requests.Session()

base_url ="https://www.akakce.com"

s_req = session.get(base_url)
print(s_req.text)
