import requests

URL = "https://www.akakce.com"
session = requests.Session()

req = session.get(URL)
print(req)