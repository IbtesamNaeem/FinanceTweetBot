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

    return tweet.strip()

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

    return tweet.strip()