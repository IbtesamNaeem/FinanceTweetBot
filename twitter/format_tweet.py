import tweepy
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime  # ✅ Correct
from scraping.earnings_tradingview import main
import logging
# 🔑 Twitter API Credentials (Replace with yours)
API_KEY = "FobrIQKVyKJFCcWnRTYnWTMEa"
API_SECRET = "famTUIrCUPb3A0plkdY1BOyelurwEGKIbZ4cskmM59vyFjQRZ3"
ACCESS_TOKEN = "1883424070123048960-JrwREtPj3MwqZLZN8R3HOraibgMVi2"
ACCESS_SECRET = "XND0vZQv2iWN0Okul0SdodAYjdhvdiyXn7QauwCb2ERIU"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAR2ygEAAAAAzSYcVTiKL3mL%2FNBJFDWf847A0kU%3DEIaA9bMAYAKnzN4jvZiCQHFEueoURF51WGvsYBEJYLwdn2b0wh"

# ✅ Initialize Twitter API v2 Client
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def format_earnings_tweet(earnings_data):
    """
    Formats earnings data into a Twitter-friendly format.
    Ensures it stays within Twitter's 280-character limit.
    """
    if not earnings_data:
        return "📉 No earnings data available for today."

    tweet = "Major Earnings This Week\n\n"
    
    for data in earnings_data[:]:  # Limit to prevent exceeding tweet length
        tweet += f"📈 {data['Ticker']} | 💰 Market Cap: {data['Market Cap']}\n"
        tweet += f"📊 EPS Estimate: {data['EPS Estimate']} | Revenue Forecast: {data['Revenue Forecast']}\n"
        tweet += "—" * 30 + "\n"  # Separator for readability

    tweet += f"📅 {datetime.now().strftime('%Y-%m-%d')}"  # Add timestamp

    return tweet

def post_earnings_tweet():
    """
    Scrapes earnings data, formats it, and posts it to Twitter.
    """
    logger.info("🔄 Fetching earnings data...")
    earnings_data = main()

    if not earnings_data:
        logger.info("❌ No earnings data found. Skipping tweet.")
        return

    logger.info(f"✅ Scraped {len(earnings_data)} earnings records.")
    logger.info(f"📝 Earnings Data: {earnings_data}")  # ✅ Debug log

    tweet_text = format_earnings_tweet(earnings_data)

    try:
        logger.info("🚀 Posting tweet...")
        response = client.create_tweet(text=tweet_text)
        logger.info(f"✅ Tweet posted successfully: {response.data}")

    except tweepy.TweepyException as e:
        logger.error(f"❌ Failed to post tweet: {e}")


if __name__ == "__main__":
    post_earnings_tweet()
