import requests
session = requests.Session()

URL = "https://api.akakce.com/"

print(session.get(URL, headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}, allow_redirects=True).text)