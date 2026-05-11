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
import re
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException

SEARCH_API_URL = "https://search.costco.ca/api/apps/www_costco_ca/query/www_costco_ca_search"
SEARCH_API_KEY = "134a4023-68d5-4138-8e03-8353667d5fb3"


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
    headless = os.getenv("COSTCO_HEADLESS", "true").lower() not in ("0", "false", "no")
    use_uc = os.getenv("COSTCO_USE_UC", "true").lower() not in ("0", "false", "no")
    if use_uc and not proxy:
        try:
            from seleniumbase import Driver
            return Driver(uc=True, headless=headless, page_load_strategy="normal")
        except Exception as e:
            print(f"SeleniumBase UC driver unavailable, falling back to Chrome webdriver: {e}")

    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,2200")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-http2')
    options.add_argument('--disable-quic')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
        print(f"Routing traffic through proxy: {proxy}")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    return webdriver.Chrome(options=options)


def get_product_id_from_url(url):
    patterns = [
        r"\.product\.(\d+)\.html",
        r"/(\d+)(?:\?|$)",
        r"[?&]partNumber=(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_search_api_product(url):
    product_id = get_product_id_from_url(url)
    if not product_id:
        return None

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': SEARCH_API_KEY,
    }
    try:
        response = requests.get(
            SEARCH_API_URL,
            params={
                'expoption': 'def',
                'q': product_id,
                'locale': 'en-CA',
                'start': '0',
                'expand': 'false',
                'loc': '*',
                'rows': '5',
            },
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Search API lookup failed for {product_id}: {e}")
        return None

    docs = response.json().get('response', {}).get('docs', [])
    for doc in docs:
        if str(doc.get('group_id')) != product_id and str(doc.get('item_number')) != product_id:
            continue
        price = doc.get('item_location_pricing_salePrice')
        if price is None:
            continue
        return {
            'url': f"https://www.costco.ca/p/-/{doc.get('group_id')}",
            'name': doc.get('item_product_name') or doc.get('item_name') or '',
            'price': str(price),
            'image': doc.get('item_product_primary_image') or doc.get('item_collateral_primaryimage') or '',
            'discount': str(doc.get('item_location_pricing_discountAmount_f') or 0),
            'limited_offer': any('Limited' in pill for pill in doc.get('item_pill_attributes') or []),
            'stock': 'In stock' if str(doc.get('item_location_stockStatus', '')).lower() == 'in stock' else 'Out of stock',
            'product_id': [str(doc.get('group_id') or product_id)],
            'item_id': str(doc.get('item_number') or doc.get('item_location_itemNumber') or ''),
        }
    return None


def get_proxies():
    use_local = os.getenv("COSTCO_USE_LOCAL", "").lower() in ("1", "true", "yes")
    if use_local:
        print("Forcing local IP (no proxy).")
        return [None]

    proxies = load_proxies()
    manual_proxy = os.getenv("COSTCO_PROXY")
    if manual_proxy:
        return [manual_proxy]
    if not proxies:
        return [None]

    proxies = [p for p in proxies if validate_proxy(p)]
    return proxies or [None]


def main():
    
    # Prefer explicit URLs from costco_urls.txt; fall back to ID-based URLs
    env_urls = os.getenv("COSTCO_URLS")
    Urls = [url.strip() for url in env_urls.split(",") if url.strip()] if env_urls else read_costco_urls()
    if not Urls:
        productID = FileReader()
        Urls = getUrl(productID)

    proxies = None
    
    for url in Urls:
        api_product = get_search_api_product(url)
        if api_product:
            print(api_product['name'])
            print(api_product['image'])
            print(api_product['price'])
            print(f"Amount discount: {api_product['discount']}")
            print(api_product['stock'])
            print(api_product['product_id'])
            print(api_product['item_id'])
            both_ids(api_product['product_id'], api_product['item_id'])
            discordWebhook(
                api_product['url'],
                api_product['name'],
                api_product['price'],
                api_product['image'],
                api_product['discount'],
                api_product['limited_offer'],
                api_product['stock'],
            )
            continue

        if proxies is None:
            proxies = get_proxies()
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
    try:
        image_element = driver.find_element(By.ID, 'initialProductImage')
        image_src = image_element.get_attribute('src')
        print(image_src)
        return image_src
    except NoSuchElementException:
        print("Image element not found")
    return ''
   
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
