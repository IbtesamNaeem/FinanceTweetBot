import asyncio
import logging
from playwright.async_api import async_playwright

async def tradingview_earnings_calendar():
    """
    Navigates to Trading View's Earnings Calendar
    page and scrapes data for stocks with
    Market Cap > 100B.
    """
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            logging.info("Beginning scraping process")
            await page.goto("https://www.tradingview.com/markets/stocks-usa/earnings/", timeout=60000)
            logging.info("Navigated to Trading View's earnings calendar page")

            await page.wait_for_selector(".tv-data-table", timeout=30000)

            rows = await page.query_selector_all(".tv-data-table__row")

            earnings_data = []

            for row in rows:
                try:
                    ticker_element = await row.query_selector("[data-field-key='name']")
                    ticker_full = (await ticker_element.text_content()).strip()
                    ticker_d = ticker_full.split("\n")[0]
                    ticker = "".join(ticker_d[:-1])

                    market_cap_element = await row.query_selector("[data-field-key='market_cap_basic']")
                    market_cap = (await market_cap_element.text_content()).strip("USD")

                    # Convert Market Cap to a numeric value
                    if market_cap in ["—", "", None]:
                        market_cap_value = 0
                    elif market_cap.endswith("K"):
                        market_cap_value = float(market_cap[:-1]) * 1_000
                    elif market_cap.endswith("M"):
                        market_cap_value = float(market_cap[:-1]) * 1_000_000
                    elif market_cap.endswith("B"):
                        market_cap_value = float(market_cap[:-1]) * 1_000_000_000
                    elif market_cap.endswith("T"):
                        market_cap_value = float(market_cap[:-1]) * 1_000_000_000_000
                    else:
                        market_cap_value = float(market_cap)

                    # Skip stocks with Market Cap <= 100B
                    if market_cap_value <= 100_000_000_000:
                        continue

                    eps_estimate_element = await row.query_selector("[data-field-key='earnings_per_share_forecast_next_fq']")
                    eps_estimate = (await eps_estimate_element.text_content()).strip("USD") if eps_estimate_element else "N/A"

                    revenue_forecast_element = await row.query_selector("[data-field-key='revenue_forecast_next_fq']")
                    revenue_forecast = (await revenue_forecast_element.text_content()).strip("USD") if revenue_forecast_element else "N/A"

                    earnings_data.append({
                        "Ticker": ticker,
                        "Market Cap": market_cap,
                        "EPS Estimate": eps_estimate,
                        "Revenue Forecast": revenue_forecast
                    })

                except Exception as e:
                    logging.error(f"Error processing row: {e}")

            earnings_messages = [
                f"{data['Ticker']} | {data['Market Cap']} | {data['EPS Estimate']} | {data['Revenue Forecast']}"
                for data in earnings_data
            ]

            return earnings_messages

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return []
    
async def tradingview_econ_calendar():
    """
    Navigates to Trading View's Economics Calendar
    page and scrapes data for upcoming econ
    events.
    """
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            logging.info("Beginning Scraping Process")
            await page.goto("https://www.tradingview.com/symbols/ALLUSD/economic-calendar/", timeout=60000)
            logging.info("Navigated to Trading View's econmics calendar page")

            await page.wait_for_selector()