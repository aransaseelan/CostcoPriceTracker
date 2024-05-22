from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver

# Checklist for products: Name, Price, Image, URL
def getCurrentPrice(url):
    
    driver = webdriver.Firefox()
    time.sleep(12)
    
    # Get the page source and pass it to BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    # Find the price element
    price = get_price(soup)
    image = get_image(soup)
    name = get_name(soup)

    return price, image, name  
    
def get_price(soup):
    price_element = soup.find('span', attrs={'automation-id': 'productPriceOutput'})
    if price_element is not None:
        return price_element.text
    else:
        return None

def get_image(soup):
    image_element = soup.find('img', attrs={'automation-id': 'initialProductImage'})
    if image_element is not None:
        return image_element['src']
    else:
        return None

def get_name(soup):
    name_element = soup.find('h1', attrs={'automation-id': 'productName'})
    if name_element is not None:
        return name_element.text
    else:
        return None