import re
from modules.user_agent import user_agent
from modules.bypass import bypass
class Scraper:
    def __init__(self):
        self.base_url = "https://api.akakce.com"
        self.session = bypass.create_session(URL=self.base_url)
    
    def create_page_number(self):
        URL = f"{self.base_url}/son-alti-ayin-en-ucuz-fiyatli-urunleri/"
        req = self.session.get(URL)
        
        page_num = int(re.findall(r'<b>Sayfa: 1 \/ ([0-9]*)<\/b>', req.text)[0])
        
        return page_num