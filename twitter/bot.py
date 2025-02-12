import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import tweepy
from dotenv import load_dotenv

from twitter.tweet_format import (
    daily_premkt_earnings_tweet, 
    daily_afterhrs_earnings_tweet,
    econ_reminder_tomorrow,
    econ_reminder_weekly
)
from scraping.earnings_tradingview import scrape_todays_earnings  # Corrected import
from scraping.econ_scraper import open_earnings_calendar, click_importance, day, scrape_economics_data
from config.logger import setup_logging

logging = setup_logging("TwitterBot")

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def post_pre_market_earnings_tweet():
    """
    Fetches earnings data and formats
    the Pre-Market tweet, and prints it.
    """
    earnings_data = scrape_todays_earnings()

    pre_market_earnings = [e for e in earnings_data if e['Time'] == "Before Open"]

    if pre_market_earnings:
        daily_premkt_earnings_tweet(pre_market_earnings)
    else:
        print("No Pre-Market earnings available.")

def post_after_hours_earnings_tweet():
    """
    Fetches earnings data and formats 
    the After-Hours tweet, and prints it.
    """
    earnings_data = scrape_todays_earnings()

    after_hours_earnings = [e for e in earnings_data if e['Time'] == "After Close"]

    if after_hours_earnings: 
        daily_afterhrs_earnings_tweet(after_hours_earnings)
    else:
        print("No After-Hours earnings available.")

def post_daily_econ_tweet():
    """
    Fetches economic data for tomorrow and 
    prints the formatted tweet.
    """
    driver = open_earnings_calendar()

    if driver:
        click_importance(driver)
        day(driver, "Tomorrow")
        time.sleep(1)
        econ_data_tomorrow = scrape_economics_data(driver)

        print("\n📊 Economic Events for Tomorrow:")
        econ_reminder_tomorrow(econ_data_tomorrow)

        driver.quit()

def post_weekly_econ_tweet():
    """
    Fetches economic data for this week and
    prints the formatted tweet.
    """
    driver = open_earnings_calendar()

    if driver:
        click_importance(driver)
        day(driver, "This Week")
        time.sleep(1)
        econ_data_week = scrape_economics_data(driver)

        print("\n📈 Economic Events for This Week:")
        econ_reminder_weekly(econ_data_week)

        driver.quit()


if __name__ == "__main__":
    print("\n🚀 Running Economic & Earnings Tweet Simulation...\n")

    post_daily_econ_tweet()
    post_weekly_econ_tweet()

    post_pre_market_earnings_tweet()
    post_after_hours_earnings_tweet()
