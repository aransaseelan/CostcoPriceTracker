from bs4 import BeautifulSoup
from DiscordWebhook import discordWebhook
import requests
import logging

class get_soup():
    elements_tags_ids = [['img', 'initialProductImage']]
    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'} # Define the headers for the request
        self.soup = self.fetch_soup() # Fetch the soup object on initialization of the class instance using the given URL
        self.process_elements()
    
    def fetch_soup(self):
        """Fetch and return BeautifulSoup object for the given URL."""
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()  # Check if the request was successful
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"HTTP request failed: {e}")
            return None  # Return None if there is an exception
    
    def find_element_by_id(self, soup, element_tag, element_id):
        """Find and return an element by tag and ID."""
        element = soup.find(element_tag, {'id': element_id})
        if not element:
            logging.warning(f"Element with tag '{element_tag}' and id '{element_id}' not found.")
            logging.debug(f"HTML content for debugging:\n{soup.prettify()}")
        return element
    
    def process_elements(self):
        elements = []
        for element_tag, element_id in self.elements_tags_ids:
            element = self.find_element_by_id(self.soup, element_tag, element_id)            
            if element:
                elements.append(element['src'])
        if elements:
            discordWebhook(self.url, elements)
    
    