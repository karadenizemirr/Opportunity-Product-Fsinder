import re
import time
import os
import pandas as pd
from datetime import datetime
from modules.user_agent import user_agent
from modules.bypass import bypass
from modules.telegram import telegram
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress

class Scraper:
    def __init__(self):
        self.base_url = "https://api.akakce.com"
        self.session = bypass.create_session(URL=self.base_url)
        self.console = Console()
        self.telegram = telegram.Telegram(token="5750542194:AAHUctF5ImPnjjOmobKfh7pUBsd_5ZHobG8", user_id="744777387")
        #self.telegram = telegram.Telegram(token="5901890521:AAG_9fjlySpTIQmJD-pb5wjYXC8hU-jjVvA", user_id="5669620760")
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
        
        return links
    
    def product_detail(self, URL = []):
        details = []
        
        with Progress() as progress:
            pbar = progress.add_task("[blue]Detaylar alınıyor..[/blue]", total=len(URL))
            for u in URL:
                try:
                    req = self.session.get(u)
                    
                    if req.status_code != 200:
                        new_session = bypass.create_session(URL=u)
                        req = new_session.get(u)
                    
                    # Create DATA
                    html = BeautifulSoup(req.text, "html.parser")
                    title = html.findAll("h1")[0].text
                    
                    first  = html.findAll("ul", {"class", "pl_v8 pr_v8"})[0].findAll("li")[0]
                    second  = html.findAll("ul", {"class", "pl_v8 pr_v8"})[0].findAll("li")[1]
                    
                    first_seller = None
                    if first.findAll("span", {'class': 'v_v8'})[0].img is None:
                        first_seller = first.findAll("span", {'class': 'v_v8'})[0].text
                    else:
                        alt = first.findAll("span", {'class': 'v_v8'})[0].img['alt']
                        text = first.findAll("span", {'class': 'v_v8'})[0].text

                        first_seller = alt + text

                    first_price = first.findAll('span', {'class': 'pt_v8'})[0].text

                    # Second Seller
                    second_seller = None
                    if second.findAll("span", {'class': 'v_v8'})[0].img is None:
                        second_seller = second.findAll("span", {'class': 'v_v8'})[0].text
                    else:
                        alt = second.findAll("span", {'class': 'v_v8'})[0].img['alt']
                        text = second.findAll("span", {'class': 'v_v8'})[0].text

                        second_seller = alt + text

                    second_price = second.findAll('span', {'class': 'pt_v8'})[0].text
                    # Calculate Percent
                    A = float(int(re.sub(r',[0-9]* TL', "", first_price).replace(".", "")))
                    B = float(int(re.sub(r',[0-9]* TL', "", second_price).replace(".", "")))

                    percent =((B-A) / B) * 100

                    if percent >= 25:
                        message = f""" 
                            <b>FIRSAT ÜRÜNÜ</b>
                            \n\n<a href="{u}">{title}</a>\n\n<b>İlk Satıcı: </b> {first_seller}\n<b>İlk Satıcı Fiyatı: </b> {first_price}\n<b>İkinci Satıcı: </b> {second_seller}\n<b>İkinci Satıcı Fiyatı: </b> {second_price}\n<b>Yüzdelik Fark: </b> %.2f
                        """ % percent
                        self.telegram.sendMessage(message=message)
                except:
                    time.sleep(5)
                    continue
                # End DATA

                progress.update(pbar, advance=1)
        return None