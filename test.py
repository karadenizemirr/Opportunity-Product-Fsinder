import requests
session = requests.Session()

URL = "https://api.akakce.com/"

print(session.get(URL))