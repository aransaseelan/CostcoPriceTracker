from helper import FileReader, getUrl
from DiscordWebhook import discordWebhook
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException


def main():
    
    #Reads products IDs from file and sets them into a Costco URL
    productID = FileReader()
    Urls = getUrl(productID)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    
    for url in Urls:
        try:
            driver.get(url)
        except WebDriverException:
            print("WebDriverException occurred. Retrying...")
            driver.get(url)
    
        time.sleep(8)
        name = get_name(driver)
        image = get_image(driver)
        price = get_price(driver)
        discount = get_discount(driver)
        limited_offer = limited_time_offer(driver)
        #Sends the information to the Discord Webhook
        discordWebhook(url, name, price, image, discount, limited_offer)
         
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

if __name__ == "__main__":
    main()