def getUrl(productID):
    url = []
    for i in productID:
        url.append("https://www.costco.ca/.product." + i + ".html")
    return url

def FileReader():
    with open('IDs.txt', 'r') as file:
        productIDs = file.read().splitlines()
    return productIDs