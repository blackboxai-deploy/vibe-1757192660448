import requests
from bs4 import BeautifulSoup
from utils.logger import get_logger

class BaseScraper:
    def __init__(self, search_criteria):
        self.search_criteria = search_criteria
        self.logger = get_logger(self.__class__.__name__)

    def get_page(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching page {url}: {e}")
            return None

    def scrape(self):
        raise NotImplementedError
