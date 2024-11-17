def getUrl(productID):
    url = []
    for i in productID:
        url.append("https://www.costco.ca/.product." + i + ".html")
    return url

def FileReader():
    with open('IDs.txt', 'r') as file:
        productIDs = file.read().splitlines()
    return productIDs

def write_internal_id(internal_ID):
    with open('Internal_IDs.txt', 'r') as file:
        productIDs = file.read().splitlines()
        
    if internal_ID not in productIDs:
        with open('Internal_IDs.txt', 'a') as file: 
            file.write(internal_ID + '\n')