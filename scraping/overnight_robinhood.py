import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from config.chrome_options import chrome_options 
from config.logger import setup_logging

logging = setup_logging("EarningsScraper")

crypto_holdings = ["MSTR", "BITO"]
crypto_mining = ["RIOT", "MARA", "HUT"]
blockchain_services = ["COIN","HOOD"]

stock_categories = {
    "Crypto": crypto_holdings,
    "Crypto Mining": crypto_mining,
    "Blockchain Services": blockchain_services,
}

def get_btc_price():
    """
    Fetches the price of BTC in USD
    and its 24 hour percentage change.
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json().get("bitcoin", {})
        btc_price = data.get("usd", "N/A")
        btc_change_24h = data.get("usd_24h_change", "N/A")

        return btc_price, btc_change_24h
    else:
        logging.error(f"Error fetching BTC data: {response.status_code}")
        return None, None

def check_all_stocks():
    """
    Checks the overnight price of each stock in the categories
    and filters those that dropped more than 3%.
    """
    try:
        driver = chrome_options()
        big_drops = {}

        for category, stocks in stock_categories.items():
            for stock in stocks:
                time.sleep(0.01)
                driver.get(f"https://robinhood.com/us/en/stocks/{stock}/")
                
                try:
                    price_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "sdp-market-price"))
                    )
                    price = price_element.text.strip("Overnight") if price_element else "N/A"

                    price_change_element = driver.find_element(By.ID, "sdp-price-chart-price-change")
                    price_change = price_change_element.text.strip("Overnight").strip("Today")

                    if "(" in price_change and "%" in price_change:
                        price_change = price_change.partition("(")[-1].partition(")")[0].rstrip("%").strip()
                        price_change = float(price_change)

                        if price_change < -3:
                            big_drops[stock] = {
                                "price": price,
                                "price_change": price_change,
                            }
                except Exception as e:
                    logging.error(f"Error fetching data for {stock}: {e}")

        logging.info("Finished checking all stocks.")
        return big_drops  

    except Exception as e:
        logging.error(f"Error while navigating stocks: {e}")
        return None

def crypto_markets():
    """
    If BTC moves ±5% in 24 hours, scrape the overnight prices
    for crypto-related stocks.
    """
    btc_price, btc_change_24h = get_btc_price()

    if btc_price is not None and btc_change_24h is not None:
        logging.info(f"BTC Price: ${btc_price}, 24h Change: {btc_change_24h:.2f}%")

        if abs(btc_change_24h) >= 5:
            logging.info("BTC has moved more than 5%. Scraping crypto stocks...")
            stock_drops = check_all_stocks()
            
            if stock_drops:
                logging.info(f"Stocks that dropped more than 3%: {stock_drops}")
            else:
                logging.info("No significant drops found.")
        else:
            logging.info("BTC movement is below the threshold. No need to scrape stocks.")
    else:
        logging.error("Failed to fetch BTC data.")