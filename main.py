import time
from modules import scraper
from rich.console import Console
console = Console()


def main():
    sc = scraper.Scraper()
    sc.create_product_link(21)
    

if __name__ == '__main__':
    main()
