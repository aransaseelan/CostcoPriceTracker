def FileReader():
    with open('IDs.txt', 'r') as file:
        productIDs = file.read().splitlines()
    return productIDs