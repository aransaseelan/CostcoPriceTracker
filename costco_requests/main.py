from api_calls import api_calls
import logging as logger

logger.basicConfig(level=logger.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logger.getLogger(__name__)

def main():
    with open('product_IDs.txt', 'r') as file:
        productIDs = file.read().splitlines()
    for prouductID in productIDs:
        logger.info(f"Getting price for product ID: {prouductID}")
        api_calls.get_price(prouductID)

if __name__ == "__main__":
    main()