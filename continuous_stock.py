# Standard Library
import asyncio
from datetime import datetime
from pathlib import Path
import os
from random import randint

# External Packages
import pandas as pd
from collections import deque
from dotenv import load_dotenv
import yfinance as yf

# Local Imports
from fetch import fetch_from_url
from util_logger import setup_logger

# Set up a file logger
logger, log_filename = setup_logger(__file__)


def lookup_ticker(company):
    stocks_dictionary = {
        "Tesla Inc": "TSLA",
        "General Motors Company": "GM",
        "Toyota Motor Corporation": "TM",
        "Ford Motor Company": "F",
        "Honda Motor Co": "HMC",
        
    }
    ticker = stocks_dictionary[company]
    return ticker

async def get_stock_price(ticker: str):
    logger.info("Calling get_stock_price for {ticker}}")
    stock_api_url = f"https://query1.finance.yahoo.com/v7/finance/option/{ticker}"
    logger.info(f"Calling fetch_from_url for {stock_api_url}")
    result = await fetch_from_url(stock_api_url, "json")
    logger.info(f"Data for {ticker}: {result.data}")
    #Extract the price from the returned result.data (see the fetch.py for more details)
    price = result.data["optionChain"]["result"][0]["quote"]["regularMarketPrice"]
    return price


async def update_csv_stock():
    """Update the CSV file with the latest stock prices."""
    logger.info("Calling update_csv_stock")

    try:
        # Add column headers when creating the empty CSV file for stock prices
        file_path = Path(__file__).parent.joinpath("data").joinpath("mtcars_stock.csv")
        if not os.path.exists(file_path):
            df_empty = pd.DataFrame(
                columns=["Company", "Ticker", "Time", "Price"]
            ).copy()
            df_empty.to_csv(file_path, index=False)

        # Stub: Create a simple DataFrame with static data
        df_data = pd.DataFrame({
            "Company": ["Tesla Inc", "General Motors Company", "Toyota Motor Corporation", "Ford Motor Company", "Honda Motor Co"],
            "Ticker": ["TSLA", "GM", "TM", "F", "HMC"],
            "Time": ["2023-07-25 12:00:00", "2023-07-25 12:01:00", "2023-07-25 12:02:00", "2023-07-25 12:03:00", "2023-07-25 12:04:00"],
            "Price": [700.0, 60.0, 200.00, 300.00, 150.00]
        })

        # Save stock prices to the CSV file
        logger.info(f"Saving stock prices to {file_path}")
        df_data.to_csv(file_path, index=False)

    except Exception as e:
        logger.error(f"An error occurred in update_csv_stock: {e}")
