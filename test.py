import cloudscraper

cs = cloudscraper.create_scraper()
req = cs.get("https://api.akakce.com")
print(req)