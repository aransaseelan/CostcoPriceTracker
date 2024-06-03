from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def put_postalcode(driver):
    postal_code_input = driver.find_element(By.ID, 'postal-code-input')

    # Enter the postal code
    postal_code_input.send_keys('M1T 3C4')

    # Find the submit button by its ID
    submit_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'postal-code-submit-btn')))

    # Click the submit button
    submit_button.click()