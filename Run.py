from FileReader import FileReader
from GetUrl import getUrl

def main():
    productID = FileReader()
    Urls = getUrl(productID)
    print(Urls)
    
if __name__ == "__main__":
    main()