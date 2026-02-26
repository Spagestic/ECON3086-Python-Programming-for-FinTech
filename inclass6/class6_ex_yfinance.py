# 1. Install yfinance library
# Run this in your terminal or uncomment the line below:
# pip install yfinance

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

# ─────────────────────────────────────────────
# 2. Function to get last week's prices (Mon–Fri)
# ─────────────────────────────────────────────
def get_price_lastweek(ticker):
    """
    Fetches the daily OHLCV data for a given ticker
    for the most recent completed Mon–Fri week.
    """
    today = datetime.today()

    # Find last Monday and last Friday
    # weekday(): Monday=0, Sunday=6
    days_since_monday = today.weekday() + 7   # go back to LAST week's Monday
    last_monday = today - timedelta(days=days_since_monday)
    last_friday = last_monday + timedelta(days=4)

    start_date = last_monday.strftime("%Y-%m-%d")
    end_date   = (last_friday + timedelta(days=1)).strftime("%Y-%m-%d")  # yfinance end is exclusive

    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date, interval="1d")

    if df.empty:
        print(f"⚠️  No data found for {ticker}")
        return None

    df.index = df.index.strftime("%Y-%m-%d")   # clean up the index display
    print(f"\n📈 {ticker} — {start_date} to {last_friday.strftime('%Y-%m-%d')}")
    print(df[["Open", "High", "Low", "Close", "Volume"]].to_string())

    return df

# ─────────────────────────────────────────────
# 3. Call the function for each ticker
# ─────────────────────────────────────────────
tickers = ["AAPL", "MSFT", "NVDA", "TSLA", "MS", "GS"]
data    = {}

for ticker in tickers:
    df = get_price_lastweek(ticker)
    if df is not None:
        data[ticker] = df

# ─────────────────────────────────────────────
# 4. Find the ticker with the highest weekly return
#    Return = (Friday Close - Monday Open) / Monday Open
# ─────────────────────────────────────────────
print("\n" + "="*55)
print("  Weekly Return Summary (Friday Close / Monday Open - 1)")
print("="*55)

returns = {}

for ticker, df in data.items():
    monday_open  = df["Open"].iloc[0]    # first day = Monday
    friday_close = df["Close"].iloc[-1]  # last  day = Friday

    weekly_return = (friday_close - monday_open) / monday_open * 100   # in %
    returns[ticker] = weekly_return

    print(f"  {ticker:<6}  Monday Open: {monday_open:>9.2f}  |  "
          f"Friday Close: {friday_close:>9.2f}  |  Return: {weekly_return:>+7.2f}%")

# Find the winner
best_ticker = max(returns, key=returns.get)

print("="*55)
print(f"\n🏆 Best performer last week: {best_ticker}")
print(f"   Weekly Return: {returns[best_ticker]:+.2f}%")