from scraping.earnings_tradingview import scrape_todays_earnings

def weekly_earnings_tweet():
    """
    Exceutes the weekly earnings tweet (Sunday 8pm)
    """

def daily_premkt_earnings_tweet():
    """
    Exceutes the daily earnings reminder 
    tweet (8pm day prior)
    """
    

def daily_afterhr_earnings_tweet():
    """
    Exceutes the daily earnings after the 
    bell reminder tweet
    """
    tweet = f"""
    ${ticker} has just reported its quarterly earnings:

    EPS Estimate ---> {eps_est}
    EPS Actual ---> {eps_actual} {mark}

    Revenue Estimate --> {rev_est}
    Revenue Actual --> {rev_actual} {mark}

    Profit Estimate --> {prof_est}
    Profit Actual --> {prof_actual} {mark}

    Guidance for the next quarter:
    Revenue expected at {revenue_outlook} ({outlook_mark})
    """

def reaction_to_result():
    """
    Executes the reaction to 
    earnings tweet
    """
    tweet = f"""
    ${ticker} stock has dropped {price_reaction} in reaction to the news.
    Current price: {current_price} (as of this tweet).
    """ 

def high_tweet():
    """
    Executes the 52-week-high tweet
    """
    tweet = f"""
    At some point today, all these stocks hit a new 52-week high:
    - ${stock}
    """

def low_tweet():
    """
    Executes the 52-week-low tweet
    """
    tweet = f"""
    At some point today, all these stocks hit a new 52-week low:
    - ${stock}
    """

def weekly_econ_event_tweet():
    """
    Executes the weekly econ reminder tweet
    """
    tweet = f"""
    Major economic events this week:
    - {event} ---> Estimate: {econ_est}, Prior: {econ_prior}
    """

def daily_econ_tweet():
    """
    Executes the daily economic reminder tweet
    (7:30 AM)
    """
    tweet = f"""
    Major economic evenents today:
    - {event} ---> Estimate: {econ_est}, Prior: {econ_prior}.
    """

def futures_tweet():
    """
    Executes the daily futures update tweet
    (Sunday at 6pm)
    """
    tweet = f"""
    Stock futures are back! We are getting closer to the market being open
    - S&P 500 Futures: {s%p_es}
    - Nasdaq 100 Futures: {nasdaq_nq}
    - DJI Futures: {dji_ym}
    - Russel 2000 Futures: {russel_rty}
    """

def halt_tweet():
    """
    Executes the trading halt tweet LUDP and T1
    """
    if reason == "LUDP":
        tweet = f"{stock} HAS BEEN HALTED - LAST AT {price}
    elif reason == "T1":
        tweet = f""
    tweet = f"{stock} HAS BEEN HALTED DUE TO NEWS PENDING"
    return tweet