import time
from modules import scraper
from rich.console import Console
console = Console()


def main():
    sc = scraper.Scraper()
    # Create Pagination
    page = sc.pagination()

    # Create Link
    sc.product_link(page=page)

    # Create Detail
    sc.product_detail()

    #Get Message
    #sc.telegram_messages()
    

if __name__ == '__main__':
    while True:
        main()
        time.sleep(4500)
