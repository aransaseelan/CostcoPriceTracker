import requests
import json 
import logging as logger
from  get_cookie import get_new_cookie

headers = {
    "Cookie": "invCheckPostalCode=M1R",
    "User-Agent": "PostmanRuntime/7.42.0",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

class api_calls:

    def get_price(self):
        try:
            price_api = "https://www.costco.ca/AjaxGetContractPrice?itemId=1746640&isFrozenItem=false&isRegionalPdt=false&isBundleItem=false&storeId=10302&inWarehouse=false"
            response = requests.get(price_api, headers=headers)
            print(response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.info("Cookies Expired... Refreshing Cookies")
            get_new_cookie().get_cookie(header)
            return None

    






