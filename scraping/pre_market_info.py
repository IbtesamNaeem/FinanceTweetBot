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

logging = setup_logging("MarketMoversLogger")

def open_premarket_page(url):
    """
    Navigates to the specified pre-market
    page (gainers or losers).
    """
    try:
        driver = chrome_options()
        logging.info(f"Initializing WebDriver and opening page: {url}")

        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tv-category-content"))
        )

        logging.info(f"Page loaded successfully: {url}")
        return driver

    except Exception as e:
        logging.error(f"Failed to open page {url}: {e}")
        return None
    
def premarket_data_scraper(driver):
    """
    Extracts Pre-Market gainers or
    losers data from TradingView
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
            ticker = ticker_full.split("\n")[0]

            percent_element = row.find_element(By.CSS_SELECTOR, "td:nth-child(2) span")
            percent_change = percent_element.text.strip()
            
            pre_market_data.append({"Ticker": ticker, "Pre-Market Change": percent_change})

        except Exception as e:
            logging.error(f"Error processing row: {e}")

    for stock in pre_market_data[:5]:
        print(f"{stock['Ticker']} - {stock['Pre-Market Change']}")

if __name__ == "__main__":
    # Navigate to Pre-Market Gainers
    driver = open_premarket_page("https://www.tradingview.com/markets/stocks-usa/market-movers-pre-market-gainers/")
    if driver:
        logging.info("Scraping Pre-Market Gainers data...")
        premarket_data_scraper(driver)  
        
        # Navigate to Pre-Market Gappers
        print("="*30)

        logging.info("Navigating to Pre-Market Gappers page...")
        driver.get("https://www.tradingview.com/markets/stocks-usa/market-movers-pre-market-gappers/")
        premarket_data_scraper(driver)

        print("="*30)

        # Navigate to Pre-Market Losers
        logging.info("Navigating to Pre-Market Losers page...")
        driver.get("https://www.tradingview.com/markets/stocks-usa/market-movers-pre-market-losers/")
        premarket_data_scraper(driver)

        print("="*30)

        # Navigate to After-Hours Gainers
        logging.info("Navigating to After-Hours Gainers page...")
        driver.get("https://www.tradingview.com/markets/stocks-usa/market-movers-after-hours-gainers/")
        premarket_data_scraper(driver)    

        print("="*30)

        # Navigate to After-Hours Losers
        logging.info("Navigating to After-Hours Losers page...")
        driver.get("https://www.tradingview.com/markets/stocks-usa/market-movers-after-hours-losers/")
        premarket_data_scraper(driver)  
        
        print("="*30)

        # Navigate to 52 Week Highs
        logging.info("Navigating to 52 Week High page...")
        driver.get("https://www.tradingview.com/markets/stocks-usa/market-movers-52wk-high/")
        premarket_data_scraper(driver) 

        print("="*30)

        # Navigate to 52 Week Lows
        logging.info("Navigating to 52 Week Lows page...")
        driver.get("https://www.tradingview.com/markets/stocks-usa/market-movers-52wk-low/")
        premarket_data_scraper(driver) 

        print("="*30)

        # Navigate to All Time Highs
        logging.info("Navigating to All Time Highs page...")
        driver.get("https://www.tradingview.com/markets/stocks-usa/market-movers-ath/")
        premarket_data_scraper(driver)

        print("="*30)

        # Navigate to All Time Lows
        logging.info("Navigating to All Time Lows page...")
        driver.get("https://www.tradingview.com/markets/stocks-usa/market-movers-atl/")
        premarket_data_scraper(driver) 

        driver.quit()

