import re
import time
import os
import pandas as pd
from modules.user_agent import user_agent
from modules.bypass import bypass
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress
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
                        second_seller = first.findAll("span", {'class': 'v_v8'})[0].text
                    else:
                        alt = first.findAll("span", {'class': 'v_v8'})[0].img['alt']
                        text = first.findAll("span", {'class': 'v_v8'})[0].text

                        second_seller = alt + text

                    second_price = second.findAll('span', {'class': 'pt_v8'})[0].text
                    # Calculate Percent
                    A = int(re.sub(r',[0-9]* TL', "", first_price).replace(".", ""))
                    B = int(re.sub(r',[0-9]* TL', "", second_price).replace(".", ""))

                    percent =((B-A) / B) * 100
                    

                    _info = {
                        "Ürün Adı": title,
                        "İlk Satıcı": first_seller,
                        "İlk Satıcı Fiyatı": first_price,
                        "İkinci Satıcı": second_seller,
                        "İkinci Satıcı Fiyatı": second_price,
                        "Yüzdelik Fark": "%.2f" % percent,
                        "Link": u
                    }

                    details.append(_info)

                    if IndexError:
                        _info = {
                        "Ürün Adı": title,
                        "İlk Satıcı": "null",
                        "İlk Satıcı Fiyatı": "null",
                        "İkinci Satıcı": "null",
                        "İkinci Satıcı Fiyatı": "null",
                        "Yüzdelik Fark": "0",
                        "Link": u
                    }
                    details.append(_info)
                except:
                    time.sleep(5)
                    continue
                # End DATA
                progress.update(pbar, advance=1)
        # Create Dataframe
        df = pd.DataFrame(details)
        
        # Save DF
        path = "data/data.xlsx"
        if os.path.isfile(path):
            os.remove(path)
        
        df.to_excel(path)
        return df

    def telegram_messages(self):
            API = "5843617868:AAGXSwTQZSgAruuw0afAzl4y-jq8RJzRWgI"
            USER_ID = "5669620760"

            df = pd.read_excel("data/data.xlsx")
            df = df[df['Yüzdelik Fark'] >= 25]
            df.rename(columns={'Unnamed: 0': 'Index'}, inplace=True)

            # Create Message
            code_html='*Fırsat Ürünleri*'  
            if df.empty == False:
                for i in range(len(df)):
                    for col in df.columns:
                        code_html = code_html + f'\n\n{col}:' + str((df[str(col)].iloc[i]))

            sendMessage = f"https://api.telegram.org/bot{API}/sendMessage"
            payloads = {
                "user_id":USER_ID,
                "text": code_html
            }
                
            try:
                self.session.post(sendMessage, data = payloads)
                self.console.log("Mesaj başarıyla gönderildi", style="bold green")
            except:
                self.console.log("Mesaj gönderilirken sorun meydana geldi..", style="bold red")