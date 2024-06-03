from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from postal_code_input import put_postalcode
# from selenium.webdriver.support import expected_conditions as EC 
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException




# Checklist for products: Name, Price, Image, URL
def get_elements(url):
    
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
    except WebDriverException:
        print("WebDriverException occurred. Retrying...")
        driver.get(url)
    
    #time.sleep(5)
    
    # Find the price element
    price = get_price(driver)
    name = get_name(driver)
    image = get_image(driver)

    return price, image, name  
    
def get_price(driver):
    price_element = None
    price_text = ''
    price_element = driver.find_element(By.CSS_SELECTOR, 'span[automation-id="productPriceOutput"]')
    price_text = price_element.text
    if (price_text == '- -.- -' or price_text == ''):
        put_postalcode(driver)
        price_element = driver.find_element(By.CSS_SELECTOR, 'span[automation-id="productPriceOutput"]')

    print(price_text)
    return price_text
    
    

def get_image(driver):
    image_element = driver.find_element(By.ID, 'initialProductImage')
    print(image_element.get_attribute('src'))
    return image_element.get_attribute('src')
   

def get_name(driver):
    name_element = driver.find_element(By.CSS_SELECTOR, 'h1[itemprop="name"]')
    print(name_element.text)
    return name_element.text