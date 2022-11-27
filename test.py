import requests

s = requests.Session()
req = s.get("https://api.akakce.com")

print(req)