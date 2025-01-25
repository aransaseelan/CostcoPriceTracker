from curl_cffi import requests
import time
import json

class requests_costco():
    
    def __init__(self, item_id, product_id):
        self.url = f"https://www.costco.ca/AjaxGetInventoryStatusUpdate?productId={product_id}&storeId=10302&warehouse=535-wh&inWarehouse=true"
        
        # Updated headers based on response analysis
        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Windows 7/ Chrome browser: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ',
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://www.costco.ca/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin'
        }

        self.cookies = {
            'invCheckStateCode': 'ON',
            'invCheckPostalCode': 'M1T 3B4',
            'invCheckCity': 'Scarborough',
            'C_LOC': 'CAON',
            'C_2LOC': 'true',
            'WC_PERSISTENT': 'true'
        }
        
        self.session = requests.Session(impersonate="chrome10")
        time.sleep(20)

    
    def get_costco_price(self):
        resp = self.session.get(self.url, headers=self.headers, cookies=self.cookies)
        print(resp.text)
        

   

if __name__ == "__main__":
    
    with open('costco_requests/bothIDs.txt', 'r') as file:
        bothIDs = file.read().splitlines()
    
    productIDs = []
    itemIDs = []
    
    for bothID in bothIDs:
        productID, itemID = bothID.split(',')
        productIDs.append(productID)
        itemIDs.append(itemID)
        print(productID, itemID)
        print(f"Getting price for product ID: {productID} and item ID: {itemID}")
        result = requests_costco(productID, itemID)
        result.get_costco_price()


