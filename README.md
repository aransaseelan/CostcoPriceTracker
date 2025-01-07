
# Costco Price Tracker <img width="75" alt="IMG_0671" src="https://github.com/aransaseelan/CostcoPriceTracker/assets/56369881/978e075d-e947-40bc-a8fd-45c90697cc52">

This is a project that enables tracking of product prices on Costco's website using product IDs and sends updates to a specified Discord channel via Webhook.

## Inspiration

While shopping on Amazon, I consistently used a browser extension to monitor discounts on products. Appreciating Costco's exceptional return policies and their excellent balance of price and quality, I sought a similar tool for their platform. When I discovered that no such extension existed, I decided to create one myself.

## How is it Built

- Programming Languages & Frameworks: Python, FastAPI
- Databases: PostgreSQL for storing historical price data
- Web Scraping Tools: Selenium and Selenium UC framework, API Reverse Engineering
- Continuous Deployment: GitHub Actions for automation and deployment

## Challenges I ran into 

- 
## Features
- Reads product IDs from a file and generates corresponding Costco URLs
- Retrieves product information such as name, price, image, stock, and discount
- Sends product information updates to specified Discord channels via Webhook
- Supports both scraping and API-based approaches
- Automated execution through GitHub Actions
- Separate webhooks for regular and sale items
- Error handling for network issues and rate limiting

## Installation
1. Clone the repository to your local machine.
```bash
git clone https://github.com/aransaseelan/CostcoPriceTracker.git
cd CostcoPriceTracker
```

2. Create a venv 
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```

## Configuration
1. Create `.env` in the root directory:
```env
"WEBHOOKNOSALE": "YOUR_REGULAR_WEBHOOK_URL",
"WEBHOOKSALE": "YOUR_SALE_WEBHOOK_URL"
```

## Usage
1. Add your product IDs to the `IDs.txt` file, one ID per line
2. Configure your two webhooks:
   - One webhook for products with no sale
   - Another webhook for products on sale
3. Run the script:
```bash
python App.py
```

## Finding Product IDs
1. Visit the Costco website
2. Navigate to a product page
3. The ID is usually on the right of the image and below the name of the product (See image below)
4. Copy the ID (145866) to your `IDs.txt` file, one per line

![image](https://github.com/user-attachments/assets/146a6c9d-7447-4c1d-abe6-62a19ff16bdd)


## Automation
This script can be automated to run at regular intervals using GitHub Actions. The provided `.github/workflows/python-script.yml` file is configured to run the script every 12 hours. You can adjust this interval by modifying the cron schedule.

Required GitHub Secrets:
- `WEBHOOKNOSALE`
- `WEBHOOKSALE`

## Request Based Costco Module
There is a new workflow file that uses a request-based approach to gather valuable price and stock information. Anyone can currently call the Costco Canada API. This can change over time; the best way to access these websites is by scraping them, which is more challenging for them to ban. However, scraping requires more resources, so if you need a fast way to gather information, the request-based module is better.

The IP addresses are also more likely to get banned through the request-based module. It uses a TLS fingerprint through the Selenium UC framework, but this can be clipped/banned at any time.

## Error Handling
- Automatically retries failed requests
- Handles network connectivity issues
- Manages API rate limiting
- Reports webhook delivery failures
- Logs errors for debugging

## Troubleshooting
If you encounter rate limiting:
- Increase delay between requests
- Use proxy rotation
- Switch to scraping approach

For webhook issues:
- Verify webhook URLs
- Check Discord channel permissions
- Ensure proper JSON formatting

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
