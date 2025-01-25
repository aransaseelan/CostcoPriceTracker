import tls_client
import requests 
import logging as logger
import time
import random

# Variables 
logger.basicConfig(level=logger.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logger.getLogger(__name__)


class api_calls:

    def get_price(productId: str, itemID: str):
        try: 
            price_api = f"https://www.costco.ca/AjaxGetContractPrice?itemId={itemID}&productId={productId}"
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.costco.ca/',
                'Connection': 'keep-alive'
            }
            cookies = {
                'invCheckPostalCode': 'M1T%203C4',
                'invCheckCity': 'Scarborough'
            }
            session = tls_client.Session(
                client_identifier="chrome112",
                random_tls_extension_order=True
            )
            response = session.get(price_api, cookies=cookies, headers=headers) 
            print(response.text)
            logger.info(f"Price for product ID: {productId} is {response.text}")
            print(price_api)
            time.sleep(random.randint(1, 5))
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")
            
            