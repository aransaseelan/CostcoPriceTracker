from helper import FileReader, getUrl
from get_elements import get_elements
from DiscordWebhook import discordWebhook

def main():
    
    #Reads products IDs from file and sets them into a Costco URL
    productID = FileReader()
    Urls = getUrl(productID)
    
    #Gets all the information needed for the Discord Webhook
    for url in Urls:
        product_info = get_elements(url)
        price = product_info[0]
        image = product_info[1]
        name = product_info[2]
        discount = product_info[3]
        limited_offer = product_info[4]
        #Sends the information to the Discord Webhook
        discordWebhook(url, name, price, image, discount, limited_offer)
         
if __name__ == "__main__":
    main()