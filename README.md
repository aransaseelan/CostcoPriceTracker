<img width="263" alt="IMG_0671" src="https://github.com/aransaseelan/CostcoPriceTracker/assets/56369881/978e075d-e947-40bc-a8fd-45c90697cc52">

This Python script tracks product prices on Costco's website and sends updates via Discord Webhook.

## Feature

- Reads product IDs from a file and generates corresponding Costco URLs.
- Retrieves product information such as name, price, image, stock, and discount.
- Sends product information updates to a specified Discord channel via Webhook.

## Installation

1. Clone the repository to your local machine.
2. Create a venv 
    ```sh
    python3 -m venv venv
    source venv/bin/activate
   ```
3. Install the required Python packages using pip:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Add your product IDs to the `IDs.txt` file, one ID per line.
2. Run the script

    ```sh
    python App.py
    ```

## Automation

This script can be automated to run at regular intervals using GitHub Actions. The provided `.github/workflows/python-script.yml` file is configured to run the script every 12 hours. You can adjust this interval by modifying the cron schedule.


## Request Based Costco Module 

There is a new workflow file that uses a request-based
approach to gather valuable price and stock information.
Anyone can currently call the Costco Canada API.
This can change over time; the best way to access these 
websites is by scraping them, which is more challenging for them to ban. However, scraping requires more
resources, so if you need a fast way to gather information, the request-based module is better. 

The IP addresses are also more likely to get banned through
the request-based module. It uses a TLS fingerprint 
through the Selenium UC framework, but this is can 
be clipped or banned at any time. 


## Hosting 

Currently in using docker, azure, and streamlit to give
it a frontend to users. Users can see what im
tracking and the goal is that it would be portable 
and users can make their own dashboard with an oauth
login.
## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


