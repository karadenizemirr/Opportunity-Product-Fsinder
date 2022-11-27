import re
import time
import os
from modules.user_agent import user_agent
from modules.bypass import bypass
from bs4 import BeautifulSoup
from rich.console import Console
class Scraper:
    def __init__(self):
        self.base_url = "https://api.akakce.com"
        self.session = bypass.create_session(URL=self.base_url)
        self.console = Console()

    def create_page_number(self):
        URL = f"{self.base_url}/son-alti-ayin-en-ucuz-fiyatli-urunleri/"
        req = self.session.get(URL)
        
        page_num = int(re.findall(r'<b>Sayfa: 1 \/ ([0-9]*)<\/b>', req.text)[0])
        
        return page_num

    def create_product_link(self, page_number):
        path = "data/links.txt"
        links = []
        with self.console.status("[blue]Linkler alınıyor..[/blue]") as status:
            for p in range(1, page_number+1):
                try:
                    if p <= 1:
                        req = self.session.get(f"{self.base_url}/son-alti-ayin-en-ucuz-fiyatli-urunleri/")
                    elif p > 1:
                        req = self.session.get(f"{self.base_url}/son-alti-ayin-en-ucuz-fiyatli-urunleri/?p={p}", allow_redirects=False)
                    
                    html = BeautifulSoup(req.text, 'html.parser').findAll("ul", {'class', 'pl_v9 gv_v9'})[0]
                    
                    for h in html:
                        links.append(f"{self.base_url}/{h.a['href']}".strip())
                except:
                    self.console.log("Bir sorun meydana geldi.", style="bold red")
                    continue
            self.console.log("Link alma işlemi tamamlandı.")
        
        # Delete File
        if os.path.isfile(path):
            os.remove(path)

        # Save File
        with open(path , "w", encoding="UTF-8") as file:
            for link in links:
                file.write("\n")
                file.write(str(link).strip())
                