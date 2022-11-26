import requests
import cloudscraper

URL = "https://akakce.com/"

headers = {
    "referer": "https://api.akakce.com/",
    "user-agent": "3.05",
    "accept": "application/json",
    "content-length": "0",
    "accept-encoding": "gzip"
}

s = requests.Session()
sc = cloudscraper.create_scraper(sess=s)

print(sc.post(URL, headers = headers))
