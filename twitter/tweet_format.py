from scraping.earnings_tradingview import scrape_todays_earnings

def weekly_earnings_tweet():
    """
    Exceutes the weekly earnings tweet (Sunday 8pm)
    """

def daily_premkt_earnings_tweet(earnings_list):
    """
    Formats the earnings reminder tweet (before market open).
    """
    tweet = "📢 Major companies reporting earnings today after the bell:\n\n"

    for stock in earnings_list:
        tweet += f"- ${stock['Ticker']} --->\n"
        tweet += f"  📊 EPS estimate: {stock['EPS Estimate']}\n"
        tweet += f"  💰 Revenue estimate: {stock['Revenue Estimate']}\n\n"

    return tweet.strip()

def daily_afterhrs_earnings_tweet(stock):
    """
    Formats the earnings results tweet after the report.
    """
    tweet = f"🚨 ${stock['Ticker']} has just reported its quarterly earnings:\n\n"

    tweet += f"📊 EPS Estimate ---> {stock['EPS Estimate']}\n"
    tweet += f"📈 EPS Actual ---> {stock['EPS Reported']} {get_beat_miss(stock['EPS Estimate'], stock['EPS Reported'])}\n\n"

    tweet += f"💰 Revenue Estimate ---> {stock['Revenue Estimate']}\n"
    tweet += f"💵 Revenue Actual ---> {stock['Revenue Reported']} {get_beat_miss(stock['Revenue Estimate'], stock['Revenue Reported'])}\n"

    return tweet.strip()

def get_beat_miss(estimate, reported):
    """
    Determines if the reported value is a BEAT, MISS, or inline
    with the analyst consensus.
    """
    try:
        estimate = float(estimate.replace("$", "").replace("B", "").replace("M", ""))
        reported = float(reported.replace("$", "").replace("B", "").replace("M", ""))

        if reported > estimate:
            return "✅ BEAT"
        elif reported < estimate:
            return "❌ MISS"
        else:
            return "🔹 Inline"
    except:
        return ""
    
def send_tweet(tweet):
    """
    Sends the tweet.
    """
    print(tweet) 

