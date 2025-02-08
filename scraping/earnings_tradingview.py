import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options
from config.logger import setup_logging
from scraping.edgar_scraper import get_latest_earnings
from twitter.tweet_format import daily_premkt_earnings_tweet, daily_afterhr_earnings_tweet, send_tweet

logging = setup_logging("EarningsScraper")

def earnings_to_be_tracked():
    """
    Returns a dictionary mapping days
    of the week to the stocks being tracked.
    """
    return {
        "Monday": ["AAPL", "TSN", "PLTR", "KD"],
        "Tuesday": ["PYPL", "AMD", "GOOGL", "SNAP"],
        "Wednesday": ["UBER", "DIS", "QCOM", "F"],
        "Thursday": ["LLY", "RBLX", "COP", "AMZN"],
        "Friday": ["CGC", "PAA", "FLO", "NWL"]
    }

def get_todays_stocks():
    """
    Returns the stock list for today's earnings
    """
    today = datetime.datetime.now().strftime("%A")
    return set(earnings_to_be_tracked().get(today, []))

def open_earnings_calendar():
    """
    Navigates to the Trading View
    Earnings calendar page.
    """
    try:
        driver = chrome_options()
        logging.info("Opening TradingView earnings calendar.")

        driver.get("https://www.tradingview.com/markets/stocks-usa/earnings/")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tv-data-table"))
        )

        logging.info("Earnings calendar loaded successfully.")
        return driver

    except Exception as e:
        logging.error(f"Failed to open earnings calendar: {e}")
        return None

def scrape_earnings_data(driver):
    """
    Extracts earnings data from TradingView and filters for today's tracked stocks.
    """
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tv-data-table"))
    )

    rows = driver.find_elements(By.CLASS_NAME, "tv-data-table__row")
    earnings_data = []
    tracked_stocks = get_todays_stocks()

    for row in rows:
        try:
            ticker_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='name']")
            ticker_full = ticker_element.text.strip()
            ticker = ticker_full.split("\n")[0].strip()

            if ticker in tracked_stocks:
                eps_estimate_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='earnings_per_share_forecast_next_fq']")
                eps_estimate = eps_estimate_element.text.strip() if eps_estimate_element else "N/A"

                revenue_forecast_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='revenue_forecast_next_fq']")
                revenue_forecast = revenue_forecast_element.text.strip() if revenue_forecast_element else "N/A"

                earnings_data.append({
                    "Ticker": ticker,
                    "EPS Estimate": eps_estimate,
                    "Revenue Estimate": revenue_forecast
                })

        except Exception as e:
            logging.error(f"Error processing row: {e}")

    return earnings_data

def post_earnings_reminder():
    """
    Posts an earnings reminder tweet before 
    the companies report.
    """
    driver = open_earnings_calendar()
    if not driver:
        logging.error("WebDriver initialization failed.")
        return

    try:
        earnings_estimates = scrape_earnings_data(driver)
        driver.quit()

        if earnings_estimates:
            for stock in earnings_estimates:
                send_tweet(daily_premkt_earnings_tweet(stock))
            logging.info("Tweeted earnings reminder.")

    except Exception as e:
        logging.error(f"Error scraping earnings estimates: {e}")

def post_earnings_results():
    """
    Fetches reported earnings from EDGAR
    and posts the final results.
    """
    tracked_stocks = get_todays_stocks()

    for ticker in tracked_stocks:
        earnings_data = get_latest_earnings(ticker)
        if earnings_data:
            send_tweet(daily_afterhr_earnings_tweet(earnings_data))
            logging.info(f"Tweeted earnings results for {ticker}.")
