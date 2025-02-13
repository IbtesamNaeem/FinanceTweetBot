import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import tweepy
from dotenv import load_dotenv

from scraping.earnings_tradingview import scrape_todays_earnings
from scraping.econ_scraper import open_earnings_calendar, click_importance, day, scrape_economics_data
from scraping.market_movers import open_premarket_page, premarket_data_scraper
from twitter.tweet_format import (
    daily_premkt_earnings_tweet,   
    daily_afterhrs_earnings_tweet, 
    econ_reminder_tomorrow,
    econ_reminder_weekly,   
    pre_market_gainer,
    pre_market_losers,
    week_high_52,
    week_low_52,
    all_time_high,
    all_time_low,
    pre_market_gap
)

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


def post_pre_market_gainers_tweet():
    """
    Fetches and posts the Pre-Market Gainers tweet.
    """
    driver = open_premarket_page("https://www.tradingview.com/markets/stocks-usa/market-movers-pre-market-gainers/")
    
    if driver:
        gainers_data = premarket_data_scraper(driver)
        pre_market_gainer(gainers_data)
        driver.quit()

def post_pre_market_losers_tweet():
    """
    Fetches and posts the Pre-Market Losers tweet.
    """
    driver = open_premarket_page("https://www.tradingview.com/markets/stocks-usa/market-movers-pre-market-losers/")
    
    if driver:
        losers_data = premarket_data_scraper(driver)
        pre_market_losers(losers_data)
        driver.quit()

def post_week_high_52_tweet():
    """
    Fetches and posts the 52-Week Highs tweet.
    """
    driver = open_premarket_page("https://www.tradingview.com/markets/stocks-usa/market-movers-52wk-high/")
    
    if driver:
        high_52_data = premarket_data_scraper(driver)
        week_high_52(high_52_data)
        driver.quit()

def post_week_low_52_tweet():
    """
    Fetches and posts the 52-Week Lows tweet.
    """
    driver = open_premarket_page("https://www.tradingview.com/markets/stocks-usa/market-movers-52wk-low/")
    
    if driver:
        low_52_data = premarket_data_scraper(driver)
        week_low_52(low_52_data)
        driver.quit()

def post_all_time_high_tweet():
    """
    Fetches and posts the All-Time Highs tweet.
    """
    driver = open_premarket_page("https://www.tradingview.com/markets/stocks-usa/market-movers-ath/")
    
    if driver:
        all_time_high_data = premarket_data_scraper(driver)
        all_time_high(all_time_high_data)
        driver.quit()

def post_all_time_low_tweet():
    """
    Fetches and posts the All-Time Lows tweet.
    """
    driver = open_premarket_page("https://www.tradingview.com/markets/stocks-usa/market-movers-atl/")
    
    if driver:
        all_time_low_data = premarket_data_scraper(driver)
        all_time_low(all_time_low_data)
        driver.quit()

def post_gap_tweet():
    """
    Fetches and posts the pre-market gapping tweet.
    """
    driver = open_premarket_page("https://www.tradingview.com/markets/stocks-usa/market-movers-pre-market-gappers/")
    
    if driver:
        pre_market_gap_data = premarket_data_scraper(driver)
        pre_market_gap(pre_market_gap_data)
        driver.quit()

if __name__ == "__main__":
    logging.info("\nRunning Market Movers Tweet Simulation...\n")

    # post_pre_market_gainers_tweet()
    # post_pre_market_losers_tweet()
    # post_week_high_52_tweet()
    # post_week_low_52_tweet()
    # post_all_time_high_tweet()
    # post_all_time_low_tweet()
    # post_gap_tweet()
    
    logging.info("\nRunning Earnings & Economic Tweet Simulation...\n")

    post_pre_market_earnings_tweet() 
    post_after_hours_earnings_tweet()  

    post_daily_econ_tweet()           
    post_weekly_econ_tweet()          
