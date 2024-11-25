from seleniumbase import SB
import time
import random
import csv
import os 
from dotenv import load_dotenv

dotenv_path = 'stockx_favourites/.env_stockx'

load_dotenv(dotenv_path=dotenv_path)

username = os.getenv('STOCKX_USERNAME')
password = os.getenv('STOCKX_PASSWORD')

with SB(uc=True) as sb:

    url = "https://accounts.stockx.com/login"
    sb.uc_open_with_reconnect(url, 4)
    sb.uc_gui_click_captcha()

    # Login to StockX
    sb.type('#email-login', username)
    sb.wait(random.randint(2, 10))
    sb.type('#password-login', password)
    # Enter email into the input field
    
    sb.click('#btn-login')
    sb.wait(random.randint(2, 10))

    sb.open("https://stockx.com/favorites/all-favorites")

    sb.wait(random.randint(2, 10))

    while True:
        try:
            sb.click('button.css-1jepaz9')
            sb.wait(random.randint(7,19)) 
        except Exception as e:
            print("No more buttons to click:", e)
            break

    sb.wait(20)

    try:
        product_elements = sb.find_elements("div.css-xlavhd")
        print(f"Found {len(product_elements)} favorite products.")
    except Exception as e:
        print("Error finding product elements:", e)
        product_elements = []
    
    favorites_data = []
    for idx, product in enumerate(product_elements, start=1):
        try:
            name_element = product.find_element("css selector", "p.chakra-text.css-1eiq52s")
            product_name = name_element.text.strip()
            
            price_element = product.find_element("css selector", "p.chakra-text.css-wukdwz")
            product_price = price_element.text.strip()

            # Extract Size by Parsing Parent Element's Text
            # After getting the parent, find the sibling span or other element containing the size
            size_parent = product.find_element("xpath", ".//span[contains(text(), 'Size')]/parent::*")
            full_text = size_parent.text 

            size = full_text.split(":")[-1].strip()

            favorites_data.append({
                'Product Name': product_name ,
                'Buy Now Price (No HST + Shipping)': product_price,
                'Product Size': size
            })
            
            print(f"Extracted {idx}: {product_name}, {product_price}, {size}")
        
        except Exception as e:
            print(f"Error extracting data for product {idx}: {e}")
            continue
    
    csv_file = 'favorites.csv'
    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            csv_headers = ['Product Name', 'Buy Now Price (No HST + Shipping)', 'Product Size']
            writer = csv.DictWriter(file, fieldnames=csv_headers)
            writer.writeheader()
            for data in favorites_data:
                writer.writerow(data)
        print(f"Successfully saved favorites data to {csv_file}")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
    