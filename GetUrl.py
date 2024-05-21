def getUrl(productID):
    url = []
    for i in productID:
        url.append("https://www.costco.ca/.product." + i + ".html")
    return url