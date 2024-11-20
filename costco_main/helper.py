

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
    with open('costco_main/IDs.txt', 'r') as file:
        productIDs = file.read().splitlines()
        
    if item_ID not in productIDs:
        with open('costco_main/IDs.txt', 'a') as file: 
            file.write(item_ID + '\n')

