import time
from modules import scraper
from rich.console import Console
console = Console()


def main():
    sc = scraper.Scraper()
    

if __name__ == '__main__':
    while True:
        main()
        time.sleep(60 * 30)
