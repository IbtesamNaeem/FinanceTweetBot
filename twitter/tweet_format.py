from scraping.econ_scraper import open_earnings_calendar, click_importance, day, scrape_economics_data

def daily_premkt_earnings_tweet(earnings_list):
    """
    Formats the Pre-Market earnings reminder tweet.
    """
    if not earnings_list:
        return "No major earnings reports scheduled for today before the bell."

    tweet = "Major companies reporting earnings TODAY BEFORE the bell:\n\n"

    for stock in earnings_list:
        tweet += f"- ${stock['Ticker']} --->\n"
        tweet += f"  EPS estimate: {stock['EPS Estimate']}\n"
        tweet += f"  Revenue estimate: {stock['Revenue Forecast']}\n\n"

    print(tweet)

def daily_afterhrs_earnings_tweet(earnings_list):
    """
    Formats the After-Market earnings reminder tweet.
    """
    if not earnings_list:
        return "No major earnings reports scheduled for today after the bell."

    tweet = "Major companies reporting earnings TODAY AFTER the bell:\n\n"

    for stock in earnings_list:
        tweet += f"- ${stock['Ticker']} --->\n"
        tweet += f"  EPS estimate: {stock['EPS Estimate']}\n"
        tweet += f"  Revenue estimate: {stock['Revenue Forecast']}\n\n"

    print(tweet)

def econ_reminder_tomorrow(econ_list):
    """
    Formats the economic event reminder tweet for TOMORROW.
    """
    if not econ_list:
        return "No major economic events scheduled for tomorrow."

    tweet = "Major economic events TOMORROW:\n\n"

    for event in econ_list:
        tweet += f"- {event['Event']}\n"

    print(tweet)

def econ_reminder_weekly(econ_list):
    """
    Formats the economic event reminder tweet for THIS WEEK.
    """
    if not econ_list:
        return "No major economic events scheduled for this week."

    tweet = "Major economic events THIS WEEK:\n\n"

    for event in econ_list:
        tweet += f"- {event['Event']}\n"

    print(tweet)

