from helper import FileReader, getUrl, both_ids, read_costco_urls
import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)
from pathlib import Path
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)

import random
from DiscordWebhook import discordWebhook
from selenium.webdriver.common.by import By
import time
import logging as logger
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException


def load_proxies():
    proxies_path = Path(__file__).resolve().parent.parent / "proxies.txt"
    if not proxies_path.exists():
        return []
    with open(proxies_path, "r") as f:
        raw = [line.strip() for line in f if line.strip()]
    user = os.getenv("COSTCO_PROXY_USER")
    password = os.getenv("COSTCO_PROXY_PASS")
    if user and password:
        enriched = []
        for p in raw:
            if "@" in p:
                enriched.append(p)
                continue
            if "://" in p:
                scheme, rest = p.split("://", 1)
            else:
                scheme, rest = "http", p
            enriched.append(f"{scheme}://{user}:{password}@{rest}")
        return enriched
    return raw


def validate_proxy(proxy: str) -> bool:
    if not proxy:
        return True
    try:
        resp = requests.get(
            "https://www.costco.ca/favicon.ico",
            proxies={"http": proxy, "https": proxy},
            timeout=8,
        )
        resp.raise_for_status()
        return True
    except Exception as e:
        print(f"Proxy validation failed ({proxy}): {e}")
        return False


def build_driver(proxy=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-http2')
    options.add_argument('--disable-quic')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
        print(f"Routing traffic through proxy: {proxy}")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    return webdriver.Chrome(options=options)


def main():
    
    # Prefer explicit URLs from costco_urls.txt; fall back to ID-based URLs
    Urls = read_costco_urls()
    if not Urls:
        productID = FileReader()
        Urls = getUrl(productID)

    use_local = os.getenv("COSTCO_USE_LOCAL", "").lower() in ("1", "true", "yes")
    if use_local:
        proxies = [None]
        print("Forcing local IP (no proxy).")
    else:
        proxies = load_proxies()
        manual_proxy = os.getenv("COSTCO_PROXY")
        if manual_proxy:
            proxies = [manual_proxy]
        elif not proxies:
            proxies = [None]
        else:
            proxies = [p for p in proxies if validate_proxy(p)]
            if not proxies:
                proxies = [None]
    
    for url in Urls:
        random.shuffle(proxies)
        last_error = None
        loaded = False
        for proxy in proxies:
            driver = build_driver(proxy)
            try:
                driver.get(url)
                time.sleep(8)
                name = get_name(driver)
                image = get_image(driver)
                price = get_price(driver)
                discount = get_discount(driver)
                limited_offer = limited_time_offer(driver)
                stock = check_stock(driver)
                product_id = get_product_id(driver)
                data_catentry = get_item_id(driver)
                both_ids(product_id, data_catentry)
                #Sends the information to the Discord Webhook
                discordWebhook(url, name, price, image, discount, limited_offer, stock)
                loaded = True
                driver.quit()
                break
            except (TimeoutException, WebDriverException) as e:
                last_error = e
                print(f"Proxy failed ({proxy}): {e}")
                driver.quit()
                continue
        if not loaded:
            print(f"All proxies failed for {url}. Last error: {last_error}")

     
def get_price(driver):
    price_element = None
    price_text = ''
    
    try:
        price_element = driver.find_element(By.CSS_SELECTOR, 'span[automation-id="productPriceOutput"]')
        price_text = price_element.text
        if (price_text == '- -.- -' or price_text == ''):
            accept_cookies(driver)
            time.sleep(10)
            price_element = driver.find_element(By.CSS_SELECTOR, 'span[automation-id="productPriceOutput"]')
            if (price_element.text == '- -.- -' or price_element.text == ''):
                put_postalcode(driver)
                # Wait until the price element is updated
                WebDriverWait(driver, 20).until_not(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'span[automation-id="productPriceOutput"]'), '- -.- -'))
                price_element = driver.find_element(By.CSS_SELECTOR, 'span[automation-id="productPriceOutput"]')
            price_text = price_element.text
    except (NoSuchElementException, ElementNotInteractableException):        print("Price not found")
    print(price_text)
    return price_text
    
def get_image(driver):
    image_src = ''
    try:
        image_element = driver.find_element(By.ID, 'initialProductImage')
        print(image_element.get_attribute('src'))
    except NoSuchElementException:
        print("Image element not found")
    return image_element.get_attribute('src')
   
def limited_time_offer(driver):
    try:
        marketing_container = driver.find_element(By.CLASS_NAME, "marketing-container")
        marketing_container.find_element(By.CLASS_NAME, "PromotionalText")
        return True
    except (NoSuchElementException, ElementNotInteractableException):
        return False

def get_name(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[itemprop="name"]')))
    name_element = driver.find_element(By.CSS_SELECTOR, 'h1[itemprop="name"]')
    print(name_element.text)
    return name_element.text

def get_discount(driver):
    # Scrap the amount discount
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='disc-value']")))
        discount_element = driver.find_element("xpath", "//span[@class='disc-value']")
        discount_amount = discount_element.text
        if discount_amount == "":
            discount_amount = "0"
    except Exception as e:
        discount_amount = "No discount"
    print(f"Amount discount: {discount_amount}")
    return discount_amount

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def check_stock(driver):
    try:
        # Correcting how By.XPATH is used and selecting the input element
        stock_element = driver.find_element(By.XPATH, '//input[@id="add-to-cart-btn" and @automation-id="addToCartButton" and @name="add-to-cart" and contains(@class, "primary-button-v2")]')
        
        # Instead of using .text, use .get_attribute('value') to get the button's text
        stock_text = stock_element.get_attribute("value")
        print(stock_text)
        if stock_text == "Add to Cart":
            return "In stock"
        else:
            return "Out of stock"
    except NoSuchElementException:
        print("Stock not found")
        return "No element Found"


def accept_cookies(driver):
    # Wait until the cookies button is clickable
    accept_cookies_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    # Click the cookies button
    accept_cookies_button.click()
    print("Cookies accepted")

def put_postalcode(driver):
    postal_code_input = driver.find_element(By.ID, 'postal-code-input')
    postal_code_input.send_keys('M1T 3C4')
    submit_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'postal-code-submit-btn')))
    submit_button.click()

def get_product_id(driver, timeout=10):
    try:
        # Wait for at least one element with the name "productBeanId" to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='productBeanId']"))
        )
        
        product_id = driver.find_elements(By.XPATH, "//input[@name='productBeanId']")
        product_id = [element.get_attribute("value") for element in product_id]
        
        print(product_id)
        return product_id
    except Exception as e:
        logger.info(f"Product IDs not found - {e}")
        print(f"Product IDs not found - {e}")
        return []

def get_item_id(driver):
    try:
        # Locate the div element using its class name
        div_element = driver.find_element(By.XPATH, '//div[@class="disc hide"]')
        # Extract the data-catentry attribute value
        item_id = div_element.get_attribute('data-catentry')
        print(item_id)
        return item_id
    except NoSuchElementException:
        print("Item Id not found")
        return ""

if __name__ == "__main__":
    main()
