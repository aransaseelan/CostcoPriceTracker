from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_discount(driver):
    # Scrap the amount discount
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='disc-value']")))
        discount_element = driver.find_element("xpath", "//span[@class='disc-value']")
        discount_amount = discount_element.text
        if discount_amount == "":
            discount_amount = "0"
        print(discount_amount)
    except Exception as e:
        print(e)
        discount_amount = "No discount"
    print(f"Amount discount: {discount_amount}")
    return discount_amount