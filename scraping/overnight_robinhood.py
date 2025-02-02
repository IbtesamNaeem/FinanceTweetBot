import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
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

semi_conductors = ["NVDA", "AMD", "INTC", "TSM", "ASML", "QCOM", "AVGO", "TXN", "MU", "AMAT"]
big_tech = ["AAPL", "MSFT", "GOOG", "GOOGL", "AMZN", "META", "NFLX", "IBM", "ORCL"]
auto_industry = ["TSLA", "RIVN", "LCID", "NIO", "LI", "XPEV", "F", "GM", "ALB"]
cybersecurity = ["CRWD", "PANW", "FTNT", "ZS", "OKTA", "NET", "S"]
social_media = ["META", "SNAP", "GOOG", "GOOGL", "PINS", "ROKU"]
pharma = ["PFE", "MRNA", "BNTX", "HIMS", "JNJ", "LLY", "NVO", "BMY", "GILD", "ABBV", "AZN", "REGN", "VRTX", "BIIB", "RHHBY", "SNY"]

def go_to_robinhood():
    """
    Navigates to RobinHood's overnight
    trading hours
    """
    try: 
        driver = chrome_options()
        logging.info("Initializing Chrome")

        driver.get(f"https://robinhood.com/us/en/stocks/NVDA/")
        logging.info("Navigated to Robinhood.")
        return driver
    
    except Exception as e:
        logging.error(f"Failed to navigate to Robinhood: {e}")

# def scrape_price(driver):
#     """
#     Scrapes the stocks continuously 
#     every 10 minutes to see if any big change
#     has occured
#     """
    
#     try:
#         price_element = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//*[@id="sdp-market-price"]'))
#         )
#         price = price_element.text

#         percent_change = 