from api_calls import api_calls

def main():
    with open('/Users/aransaseelan/Desktop/Projects/CostcoPriceTracker/Internal_IDs.txt', 'r') as file:
        productIDs = file.read().splitlines()
    for prouductID in productIDs:
        api_calls().get_price(prouductID)

if __name__ == "__main__":
    main()