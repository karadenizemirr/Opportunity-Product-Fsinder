import requests
import cfscrape

class Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://api.akakce.com/"
        # Test Requests
        test_req = self.session.get(self.base_url)
        print(test_req.text)
        
