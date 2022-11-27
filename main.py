import time
from modules import scraper
from rich.console import Console
console = Console()


def main():
    sc = scraper.Scraper()
    
    page_number = sc.create_page_number()

    product_link = sc.create_product_link(page_number=page_number)

    product_detail = sc.product_detail(URL=product_link)

if __name__ == '__main__':
    while True:
        main()
        time.sleep(60 * 30)
