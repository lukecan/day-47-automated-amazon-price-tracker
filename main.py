# Import necessary libraries
from bs4 import BeautifulSoup
import requests
import smtplib
from dotenv import load_dotenv
import os

# Designate the desired price
designated_price = 150.0

# Set headers for the request
headers = {
    "Request Line": "GET/HTTP/1.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "_ga=GA1.2.2140124808.1675233895; _gid=GA1.2.1346033030.1675233895; "
              "PHPSESSID=c143f06df4322ae2284fe4668fd8f892",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/16.2 Safari/605.1.15 "
}
# URL to scrape the product information from
url = """https://www.amazon.com.tr/JETech-Kılıf-Otomatik-Uyanma-Koruyucu/dp/B0BJZ6SNHP/ref=d_deals_ic_sccl_1_4/257
    -6629822-6946419?pd_rd_w=IYWYl&content-id=amzn1.sym.c4b57d5f-b87f-4a90-8917-c3bb3d0a8736&pf_rd_p=c4b57d5f-b87f-4a90
    -8917-c3bb3d0a8736&pf_rd_r=CHS7F0NZRNHWB2WMPDRK&pd_rd_wg=dGX5q&pd_rd_r=1ab19b1a-0815-404f-8a83-da9f09fff6ea&pd_rd_i
    =B0BJZ6SNHP&th=1 """

# Make a GET request to the URL and retrieve the response
response = requests.get(url=url, headers=headers)

# Raise an exception if the request is not successful
response.raise_for_status()

# Create a BeautifulSoup object to parse the HTML response
soup = BeautifulSoup(response.text, 'html.parser')

# Select the desired information from the response
price_whole = soup.select_one(selector='#corePriceDisplay_desktop_feature_div '
                                       '> div.a-section.a-spacing-none.aok-align-center '
                                       '> span > span:nth-child(2) > span.a-price-whole')
price_fraction = soup.select_one(selector='#corePriceDisplay_desktop_feature_div > '
                                          'div.a-section.a-spacing-none.aok-align-center > span > span:nth-child('
                                          '2) '
                                          '> span.a-price-fraction')
product_name = soup.select_one(selector="#productTitle").text

# Combine the price whole and fraction into a single float value
price = f"{price_whole.text}.{price_fraction.text}"
price = price.replace(",", "")
price = float(price)

# Check if the current price is less than or equal to the designated price
if price <= designated_price:
    # Load environment variables
    load_dotenv()
    sender = os.getenv("from")
    to = os.getenv("to")
    password = os.getenv("password")
    server = os.getenv("server")

    # Set the headers for the email
    headers = f"From: {sender}\nTo: {to}\nSubject: {product_name} Price Dropped!"
    # Set the message for the email
    message = headers + f"\n\nThe price of {product_name} dropped to {price}. You can buy it from: \n {url}"
    # There was a bug so I needed to encode the message with utf-8
    message = message.encode('utf-8')
    # Send the message with smtplib
    with smtplib.SMTP(server, port=587) as connection:
        connection.starttls()
        connection.login(user=sender, password=password)
        connection.sendmail(from_addr=sender, to_addrs=to, msg=message)
