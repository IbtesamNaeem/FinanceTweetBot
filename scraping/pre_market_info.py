import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options
from config.logger import setup_logging

logging = setup_logging("GainersLogger")

def open_premarket_gainers():
    """
    Navigates to the Trading View
    Pre-Market gainers page.
    """
    try:
        driver = chrome_options()
        logging.info("Initializing WebDriver and Pre-Market gainers page.")

        driver.get("https://www.tradingview.com/markets/stocks-usa/market-movers-pre-market-gainers/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tv-category-content"))
        )

        logging.info("Pre-Market gainers page. loaded successfully.")
        return driver

    except Exception as e:
        logging.error(f"Failed to open Pre-Market gainers page.: {e}")
        return None
    
def premarket_gainers_scraper(driver):
    """
    Extracts Pre-Market gainers data from TradingView
    """
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tv-category-content"))
    )

    rows = driver.find_elements(By.XPATH, "//div[contains(@class, 'tv-category-content')]//table/tbody/tr")
    pre_market_data = []

    for row in rows:
        try:
            ticker_element = row.find_element(By.XPATH, "./td[1]//span")
            ticker_full = ticker_element.text.strip()
            ticker_symbol = ticker_full.split("\n")[0]

            percent_element = row.find_element(By.CSS_SELECTOR, "td:nth-child(2) span")
            percent_change = percent_element.text.strip()
            
            pre_market_data.append({"Ticker": ticker_symbol, "Pre-Market Change": percent_change})

        except Exception as e:
            logging.error(f"Error processing row: {e}")

    for stock in pre_market_data[:5]:
        print(f"{stock['Ticker']} - {stock['Pre-Market Change']}")

if __name__ == "__main__":
    driver = open_premarket_gainers()
    if driver:
        premarket_gainers_scraper(driver)
        driver.quit()  


