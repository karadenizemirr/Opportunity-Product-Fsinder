import requests
from modules.user_agent import user_agent
from modules.bypass import bypass
class Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://api.akakce.com"
        self.session = bypass.create_session(URL=self.base_url)

        req = self.session.get("https://api.akakce.com/son-alti-ayin-en-ucuz-fiyatli-urunleri/")
        print(req)