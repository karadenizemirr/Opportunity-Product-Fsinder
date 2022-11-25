import requests
import random
import pandas as pd

from rich.console import Console


proxy_url = "https://free-proxy-list.net/"
test_url = "https://httpbin.org/ip"
session = requests.Session()
console = Console()

def create_proxy():
    now_IP = session.get(test_url).json()['origin']

    p_req = session.get(proxy_url)
    read_html = pd.read_html(p_req.text)[0]

    https = read_html[read_html.Https == 'yes']

    with console.status("[blue]Proxy bağlantısı yapılıyor..[/blue]") as status:
        while True:
            random_proxy = https.iloc[random.randint(0, len(https))]

            proxy = {
                "https": f"{random_proxy['IP Address']}:{random_proxy['Port']}"
            }

            try:
                test_req = session.get(test_url, proxies={
                    "https": f"http://{proxy['https']}"
                }).json()
                console.print(f""" 
                    \n Eski IP: {now_IP}
                    \n Yeni IP: {test_req['origin']}
                    \n Ülke: [blue]{random_proxy['Country']}[/blue]
                """, style="bold yellow")
                return proxy
            except:
                console.log("Proxy bağlantısı başarısız oldu.", style="bold red")