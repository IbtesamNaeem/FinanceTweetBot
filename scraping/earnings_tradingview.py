import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options 
from config.logger import setup_logging

logging = setup_logging("EarningsScraper")

def earnings_to_be_tracked():
    """
    Returns a dictionary mapping days
    of the week to the stocks being tracked.
    """
    return {
        "Monday": ["SAIA", "TSN", "IDXX", "ARLP", "TWST", "JOUT", "LVRO", "NSSC", "KYO", "MRAAY",
                   "PLTR", "KD", "CLX", "RBB", "DOC", "NXPI", "BBRR", "RMBS", "FN", "FLXS"],
        "Tuesday": ["PYPL", "SPOT", "PFE", "REGN", "PEP", "MRK", "EL", "EPC", "APO",
                    "AMD", "GOOGL", "SNAP", "CMG", "ENPH", "AMGN", "EA", "LUMN", "PRU", "JNPR"],
        "Wednesday": ["UBER", "DIS", "NVO", "EQNR", "TM", "BSX", "JCI", "SWK", "ACB", "AFL",
                      "F", "QCOM", "ARM", "SYM", "AMSC", "VKTX", "ORLY", "PI", "ALGN"],
        "Thursday": ["LLY", "RBLX", "COP", "PTON", "HSY", "BMY",
                     "AMZN", "ELF", "NET", "AFRM", "FTNT", "MCHP", "PINS", "BCE", "YUM"],
        "Friday": ["CGC", "PAA", "FLO", "NWL", "AVTR", "FTV", "GRA", "BYRN", "CBOE", "KIM"]
    }

def get_todays_stocks():
    """
    Returns the stock list for today's earnings
    """
    today = datetime.datetime.now().strftime("%A")
    tracked_stocks = earnings_to_be_tracked().get(today, [])
    return set(tracked_stocks)

def open_earnings_calendar():
    """
    Navigates to the Trading View
    Earnings calendar page.
    """
    try:
        driver = chrome_options()
        logging.info("Initializing WebDriver and opening earnings calendar page.")

        driver.get("https://www.tradingview.com/markets/stocks-usa/earnings/")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tv-data-table"))
        )

        logging.info("Earnings calendar page loaded successfully.")
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
            ticker_element = WebDriverWait(row, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-field-key='name']"))
            )
            ticker_full = ticker_element.text.strip()
            ticker_d = ticker_full.split("\n")[0]
            ticker = "".join(ticker_d[:-1])

            if ticker in tracked_stocks:
                eps_estimate_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='earnings_per_share_forecast_next_fq']")
                eps_estimate = eps_estimate_element.text.strip("USD") if eps_estimate_element else "N/A"

                revenue_forecast_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='revenue_forecast_next_fq']")
                revenue_forecast = revenue_forecast_element.text.strip("USD") if revenue_forecast_element else "N/A"
                
                try:
                    time_reporting_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='earnings_release_next_time']")
                    time_reporting = time_reporting_element.get_attribute("title").strip() if time_reporting_element else "N/A"
                except:
                    time_reporting = "N/A"

                earnings_data.append({
                    "Ticker": ticker,
                    "EPS Estimate": eps_estimate,
                    "Revenue Forecast": revenue_forecast,
                    "Time": time_reporting
                })

        except Exception as e:
            logging.error(f"Error processing row: {e}")

    return earnings_data

def scrape_todays_earnings():
    """
    Scrapes today's earnings
    from TradingView.
    """
    driver = open_earnings_calendar()
    if not driver:
        logging.error("WebDriver initialization failed.")
        return []

    try:
        return scrape_earnings_data(driver)

    except Exception as e:
        logging.error(f"Error scraping earnings: {e}.")
        
