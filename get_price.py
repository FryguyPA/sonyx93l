import requests
import re
import logging
from time import sleep

# Configure logging to save the response data
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define the log format
    filename='bestbuy.log',  # Specify the log file
    filemode='w',  # Set the file mode to 'write' (overwrite existing log file)
)

# Create a logger object
logger = logging.getLogger()

# This si the URL for the TV
url = "https://www.bestbuy.com/site/sony-75-class-bravia-xr-x93l-mini-led-4k-uhd-smart-google-tv/6543516.p?skuId=6543516"

# What you paid for it ( fool! )
purchase_price = 2499.99 # What you paid for the TV

# Standard header bs
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.1234.56 Safari/537.36'}

# Lets get the data!
response = requests.get(url, headers=headers)

# Log the response so we can check the data manually
logging.info(f'{response=}')

# If we get a good response, lets parse the data
if response.status_code == 200:
    logging.info(f'{response.text=}')
    print('Saving output to logging file\n')

    # Define the regex pattern to match currentPrice
    #pattern = r'currentPrice\":\d\d\d\d\.\d\d'
    # Found a better match that had the model info included, allowed to narrow down to a single match
    pattern = r'\"model\":\"XR75X93L\",\"price\":\d{4}\.\d{2}'

    # Find all matches in the sample text
    matches = re.findall(pattern, response.text)

    # Count the matches - used this to narrow down to a best match
    wefound = len(matches)
    print(f'We found {wefound} matches\n')

    # Check the match for any price change, then report on that
    for match in matches:
        current_price = match
        # Lets grab the last 7 characters in that line
        price = match[-7:]
        # Need to convert this to a float for comparison
        price = float(price)

        # Check to see if its the same, went up, or dropped
        if price == purchase_price:
            print('Price is the same as what you paid.\n')
        elif price > purchase_price:
            print('Price went up!  Ouch! \n')
        elif price < purchase_price:
            print('Price dropped!\n')

        print(f"Price = ${price}\n\n")

    # print the response, not using this as its too long!
    #print(response.text)

# Got a bad status code, hmm - check it if this happens
else:
    print(f'Error: {response.status_code}')