

def getUrl(productID):
    url = []
    for i in productID:
        url.append("https://www.costco.ca/.product." + i + ".html")
    return url

def FileReader():
    with open('costco_main/IDs.txt', 'r') as file:
        productIDs = file.read().splitlines()
    return productIDs

def both_ids(product_id, item_id):
    combined_id = product_id[0] + ',' + item_id
    with open('costco_requests/bothIDs.txt', 'r') as file:
        existing_ids = file.read().splitlines()
        
    if combined_id not in existing_ids:
        with open('costco_requests/bothIDs.txt', 'a') as file:
            file.write(combined_id + '\n')