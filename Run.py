from FileReader import FileReader
from GetUrl import getUrl
from UrlBeautifulSoup import get_soup
from DiscordWebhook import discordWebhook

def main():
    productID = FileReader()
    Urls = getUrl(productID)
    
    for url in Urls:
        soup = get_soup(url)
    
    #Url to the Discord Webhook
    #Begins
    
    #Ends
    
    
if __name__ == "__main__":
    main()
    