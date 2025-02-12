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
        
        pre_market_data.append({
            "Ticker": ticker,
            "Percent Change": percent_change,
        })

    return pre_market_data