from bs4 import BeautifulSoup
from DiscordWebhook import discordWebhook
import requests
import time

def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    start_time = time.time()  # Record the start time
    try:
        # Sending an HTTP GET request to the URL with headers and getting the response
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful

        # Parsing the response content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Finding the image tag with the specified id
        img_tag = soup.find('img', {'id': 'initialProductImage'})
        

        if img_tag:
            print(img_tag['src'])
        else:
            print("Image tag with id 'initialProductImage' not found.")
            print("HTML content for debugging:")
            print(soup.prettify())  # Print the HTML content in a readable format

    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

    end_time = time.time()  # Record the end time
    print(f"Time taken: {end_time - start_time} seconds")
    
    discordWebhook(url, img_tag['src'])


    
