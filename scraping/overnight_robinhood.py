import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options 
from config.logger import setup_logger
import json
logger = setup_logger("EarningsScraper")

semi_conductors = ["NVDA", "AMD", "INTC", "TSM","QCOM", "AVGO", "TXN", "MU", "AMAT"]
big_tech = ["AAPL", "MSFT", "GOOG", "AMZN","NFLX", "IBM", "ORCL"]
auto_industry = ["TSLA", "RIVN", "LI", "XPEV", "F", "GM", "ALB"]
cybersecurity = ["CRWD", "PANW", "FTNT", "ZS", "OKTA", "NET", "S"]
social_media = ["META", "SNAP", "GOOGL", "PINS", "ROKU"]
pharma = ["PFE", "MRNA", "HIMS", "JNJ", "LLY", "NVO", "BMY", "GILD", "ABBV", "REGN", "VRTX", "BIIB"]

crypto_holdings = ["MSTR", "GBTC", "BITO"]
crypto_mining = ["RIOT", "MARA", "HUT", "BITF", "HIVE", "IREN", "ARBK"]
blockchain_services = ["COIN", "SQ", "PYPL", "BKKT", "NDAQ"]
crypto_semi_conductors = ["NVDA", "AMD", "INTC"]

stock_categories = {
    "Semi Conductors": semi_conductors,
    "Big Tech": big_tech,
    "Auto Industry": auto_industry,
    "Cybersecurity": cybersecurity,
    "Social Media": social_media,
    "Pharma": pharma,
    "Crypto": crypto_holdings,
    "Crypto Mining": crypto_mining,
    "Blockchain Services": blockchain_services,
    "Crypto Semi Conductors": crypto_semi_conductors
}

def check_all_stocks():
    """
    Checks the overnight price of each stock in the categories
    to see if a big change has occurred.
    """
    try:
        driver = chrome_options()

        all_stock_data = {}

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
                    price_change = price_change_element.text.strip("Overnight") if price_change_element else "N/A"

                    all_stock_data[stock] = {
                        "price": price,
                        "price_change": price_change,
                    }

                except Exception as stock_error:
                    logger.error(f"Error retrieving data for {stock}: {stock_error}")
                    all_stock_data[stock] = {
                        "price": "N/A",
                        "price_change": "N/A",
                    }

        logger.info("Finished checking all stocks.")
        return all_stock_data  

    except Exception as e:
        logger.error(f"Error while navigating stocks: {e}")
        return None

    finally:
        driver.quit()