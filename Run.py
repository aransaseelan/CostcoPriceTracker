from FileReader import FileReader
from get_url import getUrl
from UrlBeautifulSoup import get_soup
from price_checker import getCurrentPrice
from DiscordWebhook import discordWebhook

def main():
    productID = FileReader()
    Urls = getUrl(productID)
    
    for url in Urls:
        images = get_soup(url)
        prices = getCurrentPrice(url)
        
    
    #Url to the Discord Webhook
    #Begins
    
    #Ends
    
    
if __name__ == "__main__":
    main()