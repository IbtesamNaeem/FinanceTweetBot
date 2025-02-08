import requests
import logging
import re
from bs4 import BeautifulSoup
from datetime import datetime
from config.logger import setup_logging

logging = setup_logging("EDGAR_Scraper")

BASE_URL = "https://data.sec.gov/submissions/CIK{}.json"
HEADERS = {"User-Agent": "YourBotName/1.0 (your-email@example.com)"}

def get_cik(ticker):
    """
    Fetches the CIK (Central Index Key) for a given stock ticker.
    """
    cik_url = "https://www.sec.gov/files/company_tickers.json"
    response = requests.get(cik_url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        for item in data.values():
            if item["ticker"].upper() == ticker.upper():
                return str(item["cik_str"]).zfill(10)
    return None

def get_latest_earnings(ticker):
    """
    Fetches the most recent 10-Q or 8-K (earnings report) for a stock.
    """
    cik = get_cik(ticker)
    if not cik:
        logging.error(f"No CIK found for {ticker}. Skipping...")
        return None

    response = requests.get(BASE_URL.format(cik), headers=HEADERS)
    if response.status_code != 200:
        return None

    data = response.json()
    filings = data.get("filings", {}).get("recent", {})

    for idx, form in enumerate(filings["form"]):
        if form in ["10-Q", "8-K"]:
            filing_url = f"https://www.sec.gov/Archives/{filings['primaryDocument'][idx]}"
            logging.info(f"Found earnings report for {ticker}: {filing_url}")
            return {"Ticker": ticker, "Report URL": filing_url, "EPS Reported": "TBD", "Revenue Reported": "TBD"}

    return None
