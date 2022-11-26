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
        try:
            for i in range(1, page+1):
                
                if i == 1:
                    # req = self.session.get(f"{self.base_url}/son-alti-ayin-en-ucuz-fiyatli-urunleri/", headers={
                    #     "user-agent": self.user_agent
                    # })

                    req = str(create_source.source(f"{self.base_url}/son-alti-ayin-en-ucuz-fiyatli-urunleri/",))
                
                else: 
                    # req = self.session.get(f"{self.base_url}/son-alti-ayin-en-ucuz-fiyatli-urunleri/?p={i}", headers={
                    #     "user-agent": self.user_agent
                    # })

                    req = str(create_source.source(f"{self.base_url}/son-alti-ayin-en-ucuz-fiyatli-urunleri/?p={i}"))
                
                li = BeautifulSoup(req, "html.parser").findAll("ul", {'id' : 'DPL'})[0].findAll('li')
                
                for l in li:
                    links.append(f"{l.a['href']}".strip())
        except IndexError:
            #_proxy = proxy.create_proxy()
            #req = str(create_source.source(f"{self.base_url}/son-alti-ayin-en-ucuz-fiyatli-urunleri/?p={i}"), proxy=f"http://{_proxy['https']}")
            
            # self.session.proxies.update({
            #         "https": f"http://{_proxy['https']}"})
            time.sleep(5)
            
            
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

                    if re.findall(r'403 Forbidden', req):
                        product = {
                        "Ürün Adı": "Null",
                        "İlk Satıcı": "Null",
                        "İlk Satıcı Fiyatı": "Null",
                        "İkinci Satıcı": "Null",
                        "İkinci Satıcı Fiyatı": "Null",
                        "Yüzdelik Fark": "Null",
                        "Ürün Linki": l
                        }
                        time.sleep(5)   


                    html = BeautifulSoup(req, "html.parser")
                    title = html.findAll("div", {"class" :"pdt_v8"})[0].h1.text
                    all_price = html.findAll("ul", {"id" : "PL"})[0].findAll("li")

                    first_html = all_price[0]
                    second_html = all_price[1]

                    first_price = first_html.find("span", {"class": "pt_v8"}).text

                    seller = first_html.findAll("span", {"class": "v_v8"})

                    seller_name = None

                    if seller[0].img:
                        seller_name = seller[0].img['alt'] + seller[0].text
                    elif seller[0]:
                        seller_name = seller[0].text
                    else:
                        seller_name = "Satıcı Bulunamadı."

                    second_price = second_html.find("span", {"class": "pt_v8"}).text
                    second_seller = second_html.findAll("span", {"class": "v_v8"})
                    second_seller_name = None
                    
                    if second_seller[0].img:
                        second_seller_name = second_seller[0].img['alt'] + second_seller[0].text
                    elif second_seller[0]:
                        second_seller_name = second_seller[0].text
                    else:
                        second_seller_name = "Satıcı Bulunamadı"
                    
                    # Price Analysis 
                    fp = float(re.sub(r',(.*)',"",str(first_price)))
                    sp = float(re.sub(r',(.*)',"", second_price))
                    # Calculate

                    percent = ((sp - fp) / sp) * 100
                    
                    # Create Dict
                    product = {
                        "Ürün Adı": title,
                        "İlk Satıcı": seller_name,
                        "İlk Satıcı Fiyatı": first_price,
                        "İkinci Satıcı": second_seller_name,
                        "İkinci Satıcı Fiyatı": second_price,
                        "Yüzdelik Fark": "%.2f" % float(percent),
                        "Ürün Linki": l
                    }
                    
                    detail_data.append(product)
                    time.sleep(0.3)
                except:
                    product = {
                        "Ürün Adı": "Null",
                        "İlk Satıcı": "Null",
                        "İlk Satıcı Fiyatı": "Null",
                        "İkinci Satıcı": "Null",
                        "İkinci Satıcı Fiyatı": "Null",
                        "Yüzdelik Fark": "Null",
                        "Ürün Linki": l
                        }
                    time.sleep(5)
                    continue
            self.console.log("Detaylar alma işlemi tamamlandı.", style="bold yellow")
        df = pd.DataFrame(detail_data)
        # Save Df
        filename = f"data/data.xlsx"
        df.to_excel(filename)
        return df

    def telegram_messages(self):
        df = pd.read_excel("data/data.xlsx")
        df = df[df['Yüzdelik Fark'] >= 8]
        df.rename(columns={'Unnamed: 0': 'Index'}, inplace=True)
        user_id = "5669620760"
        api_key = "5843617868:AAGXSwTQZSgAruuw0afAzl4y-jq8RJzRWgI"
        #api_key = "5750542194:AAHUctF5ImPnjjOmobKfh7pUBsd_5ZHobG8"
        #user_id = "744777387"
        sendMessage = f"https://api.telegram.org/bot{api_key}/sendMessage"

        # Create Message
        code_html='*Fırsat Ürünleri*'  
        if df.empty == False:
            for i in range(len(df)):
                for col in df.columns:
                    code_html = code_html + f'\n\n{col}:' + str((df[str(col)].iloc[i]))
    
        payloads = {
            "chat_id": user_id,
            "text" :code_html
        }

        try:
            self.session.post(sendMessage, data = payloads)
            self.console.log("Mesaj başarıyla gönderildi", style="bold green")
        except:
            self.console.log("Mesaj gönderilirken sorun meydana geldi..", style="bold red")