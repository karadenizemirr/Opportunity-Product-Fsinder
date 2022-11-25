import random
from rich.console import Console

console = Console()

def random_user_agent():
    try:
        ua = []

        with open('modules/user_agent/user_agent.txt', 'r', encoding='UTF-8') as file:
            for f in file.readlines():
                ua.append(f.strip())

        rua = ua[random.randint(0,len(ua))]

        console.print("\nUser-Agent oluşturuldu.\n", style="bold green")
        return rua
    except:
        console.print("\nUser-Agent oluşturulamadı.\n", style="bold red")