""" Download stock data from Yahoo Finance
V. Ragulin - 2025-02-28
"""
import yfinance as yf
import pandas as pd
import numpy as np

# List of US stock tickers
tickers = ["AMC", "AMD", "ANY", "APP", "ARKK", "BB",
           "COIN", "DJT", "ETHE", "GBTC", "GME", "HIMS",
           "HOOD", "KOSS", "MARA", "MSTR", "NIO", "NOK",
           "NVDA", "PLTR", "SMCI", "SPCE", "TSLA"]
start_date = "2020-01-01"  # Pull some extra data at the start
end_date = "2025-02-26"

if __name__ == "__main__":

    # Pull daily historical prices over the last 5 years
    data = yf.download(tickers, start=start_date, end=end_date, group_by='Ticker')
    data.to_csv("../data/meme_stocks_5y.csv")
    print("Done")