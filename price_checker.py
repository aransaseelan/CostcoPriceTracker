from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time

def getCurrentPrice(url):
    
    driver = webdriver.Firefox()
    
    try:
        # Load the webpage
        driver.get(url)

        # Wait for additional seconds if necessary to ensure all content is loaded
        time.sleep(15)

        # Get the page source and pass it to BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'lxml')
        

        # Find the price element
        price_element = soup.find('span', attrs={'automation-id': 'productPriceOutput'})
        if price_element is not None:
            currentPrice = price_element.text
            print(currentPrice)
        else:
            print("Price element not found.")

    finally:
        # Close the WebDriver
        driver.quit()
