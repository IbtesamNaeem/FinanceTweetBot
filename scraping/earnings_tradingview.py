import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options 

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger()

def open_earnings_calendar():
    """
    Navigates to the Trading View
    Earnings calendar page.
    """
    try:
        driver = chrome_options()
        logger.info("Initializing WebDriver and opening earnings calendar page.")

        driver.get("https://www.tradingview.com/markets/stocks-usa/earnings/")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tv-data-table"))
        )

        logger.info("Earnings calendar page loaded successfully.")
        return driver

    except Exception as e:
        logger.error(f"Failed to open earnings calendar: {e}")
        return None

def convert_market_cap_to_number(market_cap):
    """
    Converts market cap strings like
    '500M', '1.2B' into numbers.
    """
    if not market_cap or market_cap in ["—", "", None]:
        return 0

    market_cap = market_cap.strip("USD").replace(",", "")
    
    try:
        if market_cap.endswith("K"):
            return float(market_cap[:-1]) * 1_000
        elif market_cap.endswith("M"):
            return float(market_cap[:-1]) * 1_000_000
        elif market_cap.endswith("B"):
            return float(market_cap[:-1]) * 1_000_000_000
        elif market_cap.endswith("T"):
            return float(market_cap[:-1]) * 1_000_000_000_000
        else:
            return float(market_cap)
    except ValueError:
        return 0

def scrape_earnings_data(driver):
    """
    Extracts earnings data from
    the TradingView earnings calendar.
    """
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tv-data-table"))
    )

    rows = driver.find_elements(By.CLASS_NAME, "tv-data-table__row")
    earnings_data = []

    for row in rows:
        try:
            ticker_element = WebDriverWait(row, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-field-key='name']"))
            )
            ticker_full = ticker_element.text.strip()
            ticker_d = ticker_full.split("\n")[0]
            ticker = "".join(ticker_d[:-1])

            market_cap_element = WebDriverWait(row, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-field-key='market_cap_basic']"))
            )
            market_cap = market_cap_element.text.strip("USD")

            # Convert Market Cap and apply filter
            market_cap_value = convert_market_cap_to_number(market_cap)
            if market_cap_value <= 200_000_000_000: 
                continue

            eps_estimate_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='earnings_per_share_forecast_next_fq']")
            eps_estimate = eps_estimate_element.text.strip("USD") if eps_estimate_element else "N/A"

            revenue_forecast_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='revenue_forecast_next_fq']")
            revenue_forecast = revenue_forecast_element.text.strip("USD") if revenue_forecast_element else "N/A"

            earnings_data.append({
                "Market Cap": market_cap,
                "Ticker": ticker,
                "EPS Estimate": eps_estimate,
                "Revenue Forecast": revenue_forecast
            })

        except Exception as e:
            logger.error(f"Error processing row: {e}")

    return earnings_data

def get_earnings_based_on_day():
    """
    Determines which earnings to scrape
    based on the current day.
    """
    # today = datetime.today().strftime('%A')
    today = "Sunday"

    if today == "Sunday":
        logger.info("Today is Sunday. Scraping this week's earnings.")
        return upcoming_week_earnings()
    else:
        logger.info(f"Today is {today}. Scraping today's earnings.")
        return scrape_todays_earnings()

def upcoming_week_earnings():
    """
    Clicks 'Next Week' filter to get 
    earnings for the upcoming week.
    """
    driver = open_earnings_calendar()
    if not driver:
        logger.error("WebDriver initialization failed.")
        return []
    
    try:
        logger.info("Clicking 'Next Week' filter...")
        week_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'itemContent-LeZwGiB6') and contains(text(), 'Next Week')]"))
        )
        week_button.click()
        time.sleep(2)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tv-data-table"))
        )

        logger.info("Successfully navigated to 'Next Week' earnings.")
        return scrape_earnings_data(driver)

    except Exception as e:
        logger.error(f"Failed to click 'Next Week' filter: {e}")
        return []
    
def scrape_todays_earnings():
    """
    Scrapes today's earnings
    from TradingView.
    """
    driver = open_earnings_calendar()
    if not driver:
        logger.error("WebDriver initialization failed.")
        return []

    try:
        time.sleep(3)
        return scrape_earnings_data(driver)

    except Exception as e:
        logger.error(f"Error scraping earnings: {e}.")

def main():
    print("\n📢 Running Earnings Scraper...\n")
    earnings_data = get_earnings_based_on_day()

    if earnings_data:
        print(f"✅ Retrieved {len(earnings_data)} earnings records.\n")
        for data in earnings_data:
            print(f"{data['Ticker']} | Market Cap: {data['Market Cap']} | EPS Estimate: {data['EPS Estimate']} | Revenue Forecast: {data['Revenue Forecast']}")
        return earnings_data  # ✅ Ensure this is returned

    else:
        print("❌ No earnings data retrieved.")
        return []  # ✅ Return an empty list instead of None


if __name__ == "__main__":
    main()
    