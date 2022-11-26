import cfscrape

cs = cfscrape.create_scraper(delay = 10)

print(cs.get("https://www.akakce.com/"))