# Price Tracker 
A Python script that tracks the price of a product on a specified website and sends an email notification if the price drops below a designated amount.

## Requirements

- Python 3.x
- Requests library
- BeautifulSoup library
- smtplib library
- dotenv library

## Configuration

To use the script, you need to set the following environment variables in a .env file:

- `from`: Your email address that will be sending the notification.
- `to`: The recipient email address to receive the notification.
- `password`: The password for the email account sending the notification.
- `server`: The server address for the email provider, e.g. smtp.gmail.com for Gmail.

## Usage

1. Clone or download this repository to your local machine.
2. Install the required libraries using pip: `pip install -r requirements.txt`.
3. Set the environment variables in the .env file as described in the Configuration section.
4. Update the `designated_price` variable with the desired price threshold.
5. Update the `url` variable with the URL of the product you want to track.
6. Run the script: main.py

## Notes


- The script uses the BeautifulSoup library to extract the product information from the website, and the selector for the price and product name elements may need to be adjusted based on the structure of the product page on the website.
