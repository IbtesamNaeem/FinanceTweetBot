import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tweepy
from dotenv import load_dotenv
from twitter.tweet_format import daily_premkt_earnings_tweet, daily_afterhrs_earnings_tweet
from scraping.earnings_tradingview import scrape_todays_earnings
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
    Fetches earnings data, formats the Pre-Market tweet, and posts it on X.
    """
    earnings_data = scrape_todays_earnings()

    post_market_earnings = [e for e in earnings_data if e['Time'] == "Before Open"]

    post_market_tweet = daily_afterhrs_earnings_tweet(post_market_earnings)

    if post_market_tweet:
        try:
            response = client.create_tweet(text=post_market_tweet)  
            logging.info("Pre-Market earnings tweet posted!", response)
        except tweepy.TweepError as e:
            logging.critical(f"Twitter API error: {e}")
    else:
        logging.error("No Pre-Market earnings available to tweet.")
    
def post_after_hours_earnings_tweet():
    """
    Fetches earnings data, formats the After-Hours tweet, and posts it on X.
    """
    earnings_data = scrape_todays_earnings()

    post_market_earnings = [e for e in earnings_data if e['Time'] == "After Close"]

    post_market_tweet = daily_afterhrs_earnings_tweet(post_market_earnings)

    if post_market_tweet:
        try:
            response = client.create_tweet(text=post_market_tweet)
            logging.info("After-Hours earnings tweet posted!", response)
        except tweepy.TweepError as e:
            logging.critical(f"Twitter API error: {e}")
    else:
        logging.error("❌ No After-Hours earnings available to tweet.")

if __name__ == "__main__":
    post_pre_market_earnings_tweet()
