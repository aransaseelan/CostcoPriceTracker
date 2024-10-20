<img width="263" alt="IMG_0671" src="https://github.com/aransaseelan/CostcoPriceTracker/assets/56369881/978e075d-e947-40bc-a8fd-45c90697cc52">

This Python script tracks product prices on Costco's website and sends updates via Discord Webhook.

## Features

- Reads product IDs from a file and generates corresponding Costco URLs.
- Retrieves product information such as name, price, image, and discount.
- Sends product information updates to a specified Discord channel via Webhook.

## Prerequisites

- Python 3.9
- Google Chrome
- ChromeDriver
- Python packages: chromedriver-autoinstaller, selenium, discord_webhook

## Installation

1. Clone the repository to your local machine.
2. Install the required Python packages using pip:

    ```sh
    pip install chromedriver-autoinstaller selenium discord_webhook
    ```

3. Install Google Chrome and ChromeDriver. If you're on Windows, you can use Chocolatey:

    ```sh
    choco install googlechrome --ignore-checksums
    choco install chromedriver --ignore-checksums
    ```

## Usage

1. Add your product IDs to the `IDs.txt` file, one ID per line.
2. Run the script:

    ```sh
    python Run.py
    ```

## Automation

This script can be automated to run at regular intervals using GitHub Actions. The provided `.github/workflows/python-script.yml` file is configured to run the script every 5 minutes. You can adjust this interval by modifying the cron schedule.

## Files and Modules

- `Run.py`: The main script that orchestrates the product tracking process.
- `FileReader.py`: Contains the `FileReader` function that reads product IDs from `IDs.txt`.
- `get_url.py`: Contains the `getUrl` function that generates Costco URLs from product IDs.
- `get_elements.py`: Contains the `get_elements` function that retrieves product information from a given URL.
- `DiscordWebhook.py`: Contains the `discordWebhook` function that sends product information to a Discord Webhook.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
