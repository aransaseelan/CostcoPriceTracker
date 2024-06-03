from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def accept_cookies(driver):
    # Wait until the cookies button is clickable
    accept_cookies_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    # Click the cookies button
    accept_cookies_button.click()
    print("Cookies accepted")