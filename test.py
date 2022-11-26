import requests
import cfscrape

scraper = cfscrape.create_scraper(delay=10)
a = scraper.get("https://www.akakce.com/")

print(a.text)