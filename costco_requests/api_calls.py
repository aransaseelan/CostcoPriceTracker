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
<<<<<<< Updated upstream
            cookies= {
                'invCheckStateCode': 'ON',
                'invCheckPostalCode': 'M1T%203C4',
                'invCheckCity': 'Scarborough',
                'STORELOCATION': '{%22storeLocation%22:{%22zip%22:%22M3K%202C8%22%2C%22city%22:%22Downsview%22}}'
=======
            cookies = {
                'invCheckPostalCode': 'M1T%203C4',
                'invCheckCity': 'Scarborough'
>>>>>>> Stashed changes
            }
            session = tls_client.Session(
                client_identifier="chrome112",
                random_tls_extension_order=True
            )
<<<<<<< Updated upstream
            response = session.get(price_api, cookies=cookies)
=======
            response = session.get(
                price_api, cookies=cookies
            )
>>>>>>> Stashed changes
            print(response.text)
            logger.info(f"Price for product ID: {productId} is {response.text}")
            print(price_api)
            time.sleep(random.randint(1, 5))
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")