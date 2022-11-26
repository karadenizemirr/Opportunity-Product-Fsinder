import cloudscraper

cs = cloudscraper.create_scraper(delay = 10)

r = cs.get("https://www.akakce.com/")
print(r)