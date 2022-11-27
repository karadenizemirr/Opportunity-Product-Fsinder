import cloudscraper

cs = cloudscraper.create_scraper(delay=10)
while True:
    req = cs.get("https://api.akakce.com")
    print(req)