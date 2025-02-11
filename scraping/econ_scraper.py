import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options
from config.logger import setup_logging

logging = setup_logging("EconScraper")

def open_earnings_calendar():
    """
    Navigates to the Trading Views
    USDCAD Economic Calendar page.
    """
    try:
        driver = chrome_options()
        driver.set_window_size(1920, 1080)

        logging.info("Initializing WebDriver and opening economic calendar page.")

        driver.get("https://www.tradingview.com/symbols/USDCAD/economic-calendar/?exchange=FX_IDC")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@data-name, 'economic-calendar-item')]"))
        )

        logging.info("Economic calendar page loaded successfully.")
        return driver

    except Exception as e:
        logging.error(f"Failed to open economic calendar: {e}")
        return None

def click_importance(driver):
    """
    Clicks the Importance filter button
    to filter out
    """
    try:
        logging.info("Finding the High Importance button.")

        importance_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="js-category-content"]/div[2]/div/section/div/div[2]/div/div/div/div[1]/div[1]/button/span[2]/span[1]'))
        )

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", importance_button)
        time.sleep(2)
        
        driver.execute_script("arguments[0].click();", importance_button)
        
        logging.info("Importance button clicked successfully.")

    except Exception as e:
        logging.error(f"Failed to click Importance button: {e}")

def scrape_economicss_data(driver):
    """
    Extracts the Economic Event data 
    from Trading View
    """
    logging.info("Waiting for the economic calendar to load.")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@data-name, 'economic-calendar-item')]"))
    )

    rows = driver.find_elements(By.XPATH, "//div[contains(@data-name, 'economic-calendar-item')]")

    if not rows:
        logging.error("No economic calendar rows found.")
        return []

    logging.info(f"Found {len(rows)} economic event rows.")

    econ_data = []

    for index, row in enumerate(rows):
        logging.info(f"Processing row {index + 1}...")

        try:
            event_element = row.find_element(By.XPATH, ".//span[contains(@class, 'titleText')]")
            event_name = event_element.text.strip()
        except Exception as e:
            event_name = "N/A"
            logging.error(f"Error extracting event name in row {index + 1}: {e}")

        logging.info(f"Event: {event_name}")

        try:
            forecast_elements = row.find_elements(By.XPATH, ".//span[contains(@class, 'value')]")
            forecast_value = forecast_elements[0].text.strip() if len(forecast_elements) > 0 else "N/A"
            
            prior_elements = row.find_elements(By.XPATH, "")
            prior_value = forecast_elements[1].text.strip() if len(forecast_elements) > 1 else "N/A"

            forecast_value = forecast_value.replace("%", "").strip()
            prior_value = prior_value.replace("%", "").strip()

        except Exception as e:
            forecast_value = "N/A"
            prior_value = "N/A"
            logging.error(f"Error extracting forecast/prior in row {index + 1}: {e}")

        logging.info(f"Forecast: {forecast_value} | Prior: {prior_value}")

        try:
            date_element = row.find_elements(By.XPATH, ".//span[contains(@class, 'economic-calendar-item-time')]")
            event_date = date_element[0].text.strip() if date_element else "N/A"

        except Exception as e:
            event_date = "N/A"
            logging.error(f"Error extracting date in row {index + 1}: {e}")

        logging.info(f"Date: {event_date}")

        econ_data.append({
            "Event": event_name,
            "Forecast": forecast_value,
            "Prior": prior_value,
            "Date": event_date
        })

    return econ_data
