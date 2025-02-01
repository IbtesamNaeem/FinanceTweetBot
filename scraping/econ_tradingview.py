import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options 
from config.logger import setup_logger

logger = setup_logger("EarningsScraper")

def open_econ_calendar():
    """
    Navigates to the Trading View and opens
    the USD/CAD economics calendar page.
    """
    try:
        driver = chrome_options()
        logger.info("Initializing WebDriver and opening economic calendar page.")

        driver.get("https://www.tradingview.com/symbols/USDCAD/economic-calendar/?exchange=FX_IDC")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-name='economicCalendar']"))
        )

        logger.info("Economic calendar page loaded successfully.")
        return driver

    except Exception as e:
        logger.error(f"Failed to open economic calendar: {e}")
        return None  

def scrape_econ_data(driver):
    """
    Extracts economic event data from
    the TradingView economic calendar.
    """
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "js-symbol-page-tab-economic-calendar"))
    )

    rows = driver.find_elements(By.CLASS_NAME, "js-symbol-page-tab-economic-calendar")
    econ_data = []

    for row in rows:
        try:
            event_element = WebDriverWait(row, 3).until(
                EC.presence_of_element_located((By.XPATH, ".//span[contains(@class, 'event-title')]"))
            )
            event_name = event_element.text.strip()

            forecast_elements = row.find_elements(By.XPATH, ".//span[contains(@class, 'valueWithUnit')]")
            forecast = forecast_elements[0].text.replace("USD", "").strip() if len(forecast_elements) > 0 else "N/A"
            prior = forecast_elements[1].text.replace("USD", "").strip() if len(forecast_elements) > 1 else "N/A"

            econ_data.append({
                "Event Name": event_name,
                "Forecast": forecast,
                "Prior": prior,
            })

        except Exception as e:
            logger.error(f"Error processing row: {e}")

    return econ_data

def get_econ_based_on_day():
    """
    Determines which economic events to scrape
    based on the current day.
    """
    # today = datetime.today().strftime('%A')
    today = "Sunday"

    if today == "Sunday":
        logger.info("Today is Sunday. Scraping this week's economics events.")
        return upcoming_week_econ()
    else:
        logger.info(f"Today is {today}. Scraping today's economics events.")
        return scrape_todays_econ()

def upcoming_week_econ():
    """
    Clicks 'Next Week' filter to get 
    economic events for the upcoming week. 
    """
    driver = open_econ_calendar()
    if not driver:
        logger.error("WebDriver initialization failed.")
        return []
    
    try:
        logger.info("Clicking 'Next Week' filter...")
        week_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'content-mf1FlhVw') and normalize-space(text())='This Week']"))
        )
        week_button.click()
        time.sleep(2)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "js-symbol-page-tab-economic-calendar"))
        )

        logger.info("Successfully navigated to 'Next Week' economics page.")
        return scrape_econ_data(driver)

    except Exception as e:
        logger.error(f"Failed to click 'Next Week' filter: {e}")
        return []

def scrape_todays_econ():
    """
    Scrapes today's economic events
    from TradingView.
    """
    driver = open_econ_calendar()
    if not driver:
        logger.error("WebDriver initialization failed.")
        return []

    try:
        time.sleep(3)
        return scrape_econ_data(driver)

    except Exception as e:
        logger.error(f"Error scraping economic events: {e}.")