import time
import logging
import requests
from datetime import datetime
from config.logger import setup_logging
from scraping.overnight_robinhood import check_all_stocks
from twitter.tweet_format import format_btc_tweet, send_tweet

logging = setup_logging("CryptoMarketBot")

crypto_holdings = ["MSTR", "BITO"]
crypto_mining = ["RIOT", "MARA", "HUT"]
blockchain_services = ["COIN", "HOOD"]

stock_categories = {
    "Crypto": crypto_holdings,
    "Crypto Mining": crypto_mining,
    "Blockchain Services": blockchain_services,
}

def get_btc_price():
    """
    Fetches the price of BTC in USD
    and its 24-hour percentage change.
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json().get("bitcoin", {})
            btc_price = data.get("usd", "N/A")
            btc_change_24h = data.get("usd_24h_change", "N/A")

            return btc_price, btc_change_24h
        else:
            logging.error(f"Error fetching BTC data: {response.status_code}")
            return None, None
        
    except Exception as e:
        logging.error(f"Error fetchign BTC price: {e}")
        return None, None
    

def crypto_markets():
    """
    If BTC moves ±5% in 24 hours, scrape crypto-related stocks and tweet.
    """
    btc_price, btc_change_24h = get_btc_price()

    if btc_price is not None and btc_change_24h is not None:
        logging.info(f"BTC Price: ${btc_price}, 24h Change: {btc_change_24h:.2f}%")

        if abs(btc_change_24h) >= 5:
            logging.info("🚀 BTC has moved more than 5%. Scraping crypto stocks...")

            stock_prices = {}
            for category in ["Crypto", "Crypto Mining", "Blockchain Services"]:
                stock_prices.update(check_all_stocks(category))

            tweet = format_btc_tweet(btc_change_24h, stock_prices)
            send_tweet(tweet)

        else:
            logging.info("BTC movement is below the threshold. No need to scrape stocks.")
    else:
        logging.error("Failed to fetch BTC data.")

