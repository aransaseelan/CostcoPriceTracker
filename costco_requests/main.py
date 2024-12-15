from api_calls import api_calls
import logging as logger

logger.basicConfig(level=logger.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logger.getLogger(__name__)

def main():
    with open('costco_requests/bothIDs.txt', 'r') as file:
        bothIDs = file.read().splitlines()
    
    productIDs = []
    itemIDs = []
    
    for bothID in bothIDs:
        productID, itemID = bothID.split(',')
        productIDs.append(productID)
        itemIDs.append(itemID)
        logger.info(f"Getting price for product ID: {productID} and item ID: {itemID}")
        api_calls.get_price(productID, itemID)

if __name__ == "__main__":
    main()