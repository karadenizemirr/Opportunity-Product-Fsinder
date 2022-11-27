import requests
import re
import time
import os
import pandas as pd
import cloudscraper
from modules.user_agent import user_agent
from rich.console import Console
from bs4 import BeautifulSoup
from modules import proxy
from modules import create_source

class Scraper:
    def __init__(self):
        self.user_agent = user_agent.random_user_agent()
        self.session = requests.Session()
        self.console = Console()
        self.base_url = "https://api.akakce.com"
        
    
    def pagination(self):
        while True:
            try:
                s_req = str(create_source.source(f"{self.base_url}/son-alti-ayin-en-ucuz-fiyatli-urunleri/"))
                page_number = re.findall(r'<b>Sayfa: 1 \/ (.*?)<\/b>', s_req)[0]
                
                return int(page_number)
            except:
                self.console.print("\nSayfa numarası alınırken bir sorun meydana geldi.\n", style="bold red")
                time.sleep(5)
    
    def product_link(self, page = 21):
        links = []
        for i in range(1, page+1):
            try:
                if i == 1:
                    req = str(create_source.source(f"{self.base_url}/son-alti-ayin-en-ucuz-fiyatli-urunleri/",))
                
                else: 
                    req = str(create_source.source(f"{self.base_url}/son-alti-ayin-en-ucuz-fiyatli-urunleri/?p={i}"))
                
                li = BeautifulSoup(req, "html.parser").findAll("ul", {'id' : 'DPL'})[0].findAll('li')
                
                for l in li:
                    links.append(f"{l.a['href']}".strip())
            except:
                time.sleep(5)
                continue
            
            
        try:
            os.remove("data/links.txt")
        except OSError:
            pass

        try:
            # Save Links File
            with open('data/links.txt', 'w', encoding="UTF-8") as file:
                for l in links:
                    file.write("\n")
                    file.write(l)
        except:
            self.console.print("\nLink dosyası oluşturulamadı.", style="bold red")
    
    def product_detail(self):
        #Open link file
        links = []
        with open("data/links.txt", "r", encoding="utf-8") as file:
            for f in file.readlines():
                links.append(f.strip())
        del links[0]

        detail_data = []
        # Get Product Detail
        
        with self.console.status("[blue]Detaylar alınıyor..[/blue]") as status:
            for l in links:
                try:
                    #req = self.session.get(l)
                    req = str(create_source.source(l))
                    
                    html = BeautifulSoup(req, "html.parser")
                    title = html.findAll("div", {"class" :"pdt_v8"})[0].h1.text
                except:
                    continue
                
            self.console.log("Detaylar alma işlemi tamamlandı.", style="bold yellow")
        df = pd.DataFrame(detail_data)
        # Save Df
        filename = f"data/data.xlsx"
        df.to_excel(filename)
        return df


    def telegram_messages(self):
        df = pd.read_excel("data/data.xlsx")
        df = df[df['Yüzdelik Fark'] >= 25]
        df.rename(columns={'Unnamed: 0': 'Index'}, inplace=True)

        print(df)
        total_user = [
            {
                "user_id": "5669620760",
                "api_key": "5843617868:AAGXSwTQZSgAruuw0afAzl4y-jq8RJzRWgI"
            },
            {
                "user_id": "744777387",
                "api_key": "5750542194"
            }
        ]

        # Create Message
        code_html='*Fırsat Ürünleri*'  
        if df.empty == False:
            for i in range(len(df)):
                for col in df.columns:
                    code_html = code_html + f'\n\n{col}:' + str((df[str(col)].iloc[i]))

        for t in total_user:
            sendMessage = f"https://api.telegram.org/bot{t['api_key']}/sendMessage"
            payloads = {
                "user_id":t['user_id'],
                "text": code_html
            }
            

        try:
            self.session.post(sendMessage, data = payloads)
            self.console.log("Mesaj başarıyla gönderildi", style="bold green")
        except:
            self.console.log("Mesaj gönderilirken sorun meydana geldi..", style="bold red")