import tls_client
import json 
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
            session = tls_client.Session(
                client_identifier="chrome112",
                random_tls_extension_order=True
            )
            response = session.get(
                price_api
            )
            print(response.text)
            logger.info(f"Price for product ID: {productId} is {response.text}")
            time.sleep(random.randint(1, 5))
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")