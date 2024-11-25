

def getUrl(productID):
    url = []
    for i in productID:
        url.append("https://www.costco.ca/.product." + i + ".html")
    return url

def FileReader():
    with open('costco_main/IDs.txt', 'r') as file:
        productIDs = file.read().splitlines()
    return productIDs

def write_product_id(product_ID):
    with open('costco_requests/product_IDs.txt', 'r') as file:
        productIDs = file.read().splitlines()
        
    if product_ID not in productIDs:
        with open('costco_requests/product_IDs.txt', 'a') as file: 
            file.write(product_ID + '\n')

def write_item_id(item_ID):
    with open('costco_requests/item_IDs.txt', 'r') as file:
        itemIDs = file.read().splitlines()
        
    if item_ID not in itemIDs:
        with open('costco_requests/item_IDs.txt', 'a') as file: 
            file.write(item_ID + '\n')

def both_ids(product_id, item_id):
    combined_id = product_id[0] + ',' + item_id
    with open('costco_requests/bothIDs.txt', 'r') as file:
        existing_ids = file.read().splitlines()
        
    if combined_id not in existing_ids:
        with open('costco_requests/bothIDs.txt', 'a') as file:
            file.write(combined_id + '\n')