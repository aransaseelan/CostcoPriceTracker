<img width="263" alt="IMG_0671" src="https://github.com/aransaseelan/CostcoPriceTracker/assets/56369881/978e075d-e947-40bc-a8fd-45c90697cc52">

This Python script tracks product prices on Costco's website and sends updates via Discord Webhook.

<img width="263" alt="OtherImage" src="https://github.com/user-attachments/assets/4dc5942c-93dc-4479-ae78-2ca4d5ed1700">

This Python script logins into your profile, gets all your favourites and puts them into CSV formatting. 

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

There is a new workflow file which uses a request based 
approach to gather the valuable price and stock information.
The Costco Canada API is currently allowed to anyone to call.
This can change at anytime and the best way to go to these 
websites are by scraping them. This in turn requires more 
resources though if you require a fast way to gather information.
The request based module is better. 

The IP addresses are also more likely to get banned through
the request based module. It is using a TLS fingerprint 
through the Selenium UC framework but this is can 
obviously be clipped or banned at anytime. 

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


