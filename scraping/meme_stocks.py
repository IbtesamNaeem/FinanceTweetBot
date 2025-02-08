import os
import logging
import tweepy
from dotenv import load_dotenv
from scraping.overnight_robinhood import check_all_stocks
from twitter.tweet_format import format_meme_tweet, send_tweet  # Import tweet functions

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

TARGET_USERNAME = "TheRoaringKitty"
LAST_TWEET_FILE = "last_tweet.txt"

def get_user_id(username):
    """
    Fetch the user ID for the given username.
    """
    try:
        user = client.get_user(username=username, user_fields=["id"])
        return user.data.id if user.data else None
    except Exception as e:
        logging.error(f"Error fetching user ID: {e}")
        return None

def get_last_saved_tweet():
    """
    Reads the last saved tweet ID from file.
    """
    if os.path.exists(LAST_TWEET_FILE):
        with open(LAST_TWEET_FILE, "r") as file:
            return file.read().strip()
    return None

def save_last_tweet(tweet_id):
    """
    Saves the latest tweet ID to a file.
    """
    with open(LAST_TWEET_FILE, "w") as file:
        file.write(str(tweet_id))

def check_latest_tweet():
    """
    Checks to see if Roaring Kitty (DFV) has posted
    a new tweet on X.

    IF he has, then scrape Robinhood for meme stock
    prices and tweet about it.
    """
    global TARGET_USER_ID

    TARGET_USER_ID = get_user_id(TARGET_USERNAME)
    if TARGET_USER_ID is None:
        logging.error("Failed to retrieve user ID.")
        return

    try:
        response = client.get_users_tweets(
            id=TARGET_USER_ID,
            max_results=5, 
            tweet_fields=["id", "created_at"]
        )

        if response.data:
            latest_tweet = response.data[0]
            latest_tweet_id = str(latest_tweet.id)

            last_saved_tweet_id = get_last_saved_tweet()

            if last_saved_tweet_id != latest_tweet_id:
                logging.info(f"🐱 Roaring Kitty posted a new tweet! Triggering meme stock check...")

                save_last_tweet(latest_tweet_id)

                stock_prices = check_all_stocks("Meme Stocks")

                tweet = format_meme_tweet(stock_prices)
                send_tweet(tweet)

            else:
                logging.info("No new tweet from Roaring Kitty. Skipping meme stock check.")

    except Exception as e:
        logging.error(f"Error fetching tweet: {e}")
