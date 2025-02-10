import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options 
from config.logger import setup_logging

logging = setup_logging("EconScraper")

def open_econ_calendar():
    """
    Navigates to the Trading Economics
    Economics calendar page.
    """
    try:
        driver = chrome_options()
        logging.info("Initializing WebDriver and opening earnings calendar page.")

        driver.get("https://tradingeconomics.com/united-states/calendar")
        filter_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "d-none.d-lg-inline"))
        )

        logging.info("Earnings calendar page loaded successfully.")
        return driver

    except Exception as e:
        logging.error(f"Failed to open earnings calendar: {e}")
        return None
    

def select_option(driver):
    """
    Selects the "Impact" button and then clicks the
    three-star (level 3) importance checkbox. 
    """
    try:
        logging.info("Finding and clicking the Impact button.")

        impact_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ctl00_Button1"]/span'))
        )
        
        driver.execute_script("arguments[0].click();", impact_button)
        logging.info("Impact button clicked successfully.")

    except Exception as e:
        logging.error(f"Failed to click on Impact button: {e}")

    try:
        logging.info("Finding and clicking the level 3 importance checkbox.")

        level_3_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="aspnetForm"]/div[3]/div/div[1]/table/tbody/tr/td[1]/div/div[2]/ul/li[3]/a/input'))
        )

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", level_3_button)
        time.sleep(2)

        try:
            level_3_button.click()
            logging.info("Level 3 importance checkbox clicked successfully (normal click).")
        except Exception as click_error:
            logging.warning(f"Normal click failed: {click_error}. Using JavaScript click.")

            driver.execute_script("arguments[0].click();", level_3_button)
            logging.info("Level 3 importance checkbox clicked successfully (JS click).")

    except Exception as e:
        logging.error(f"Failed to press level 3 importance option: {e}.")


def scrape_econ_data(driver):
    """
    Extracts economic events from Trading Economics:
    """
    logging.info("Waiting for the economic calendar to load...")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//tr[@data-event]"))
        )

    except Exception:
        logging.error("Economic events did not load.")
        return []

    rows = driver.find_elements(By.XPATH, "//tr[@data-event]")

    if not rows:
        logging.warning("No economic events found.")
        return []

    econ_data = []

    for row in rows:
        try:
            event_name = row.get_attribute("data-event").strip()

            try:
                previous_element = row.find_element(By.XPATH, ".//td[contains(@class, 'calendar-item') and contains(@class, 'calendar-item-positive')]")
                previous_value = previous_element.text.strip() if previous_element.text else "N/A"
            except:
                previous_value = "N/A"

            try:
                forecast_element = row.find_element(By.XPATH, ".//td[contains(@class, 'calendar-item') and contains(@class, 'calendar-item-forecast')]")
                forecast_value = forecast_element.text.strip() if forecast_element.text else "N/A"
            except:
                forecast_value = "N/A"

            logging.info(f"✅ Extracted: {event_name} | Previous: {previous_value} | Forecast: {forecast_value}")

            econ_data.append({
                "Event Name": event_name,
                "Previous Value": previous_value,
                "Forecast Value": forecast_value
            })

        except Exception as e:
            logging.error(f"Error processing row: {e}")

    return econ_data
