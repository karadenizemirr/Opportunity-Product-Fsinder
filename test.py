import requests
session = requests.Session()

URL = "https://api.akakce.com/"

req = session.get(URL)

print(req.text)