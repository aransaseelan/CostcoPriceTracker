from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

def put_postalcode(driver):
    postal_code_input = driver.find_element(By.ID, 'postal-code-input')
    postal_code_input.send_keys('M1T 3C4')

    time.sleep(2)
    submit_button = driver.find_element(By.ID, 'postal-code-submit-btn')
    submit_button.click()