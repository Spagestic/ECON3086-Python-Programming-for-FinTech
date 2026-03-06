import yfinance as yf
from datetime import datetime, timedelta

def get_price_lastweek(ticker):
    # Get today's date
    today = datetime.now()
    
    # Calculate last Friday and last Monday
    last_sat = today - timedelta(days=today.weekday() + 2)
    last_monday = last_sat - timedelta(days=5)
    
    # Format dates as strings
    start_date = last_monday.strftime('%Y-%m-%d')
    end_date = last_sat.strftime('%Y-%m-%d')    

    # Get stock data from yfinance
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date)
    
    return hist

def get_returns(data):
    monday_open = data.iloc[0]['Open']
    friday_close = data.iloc[-1]['Close']
    return (friday_close - monday_open) / monday_open * 100

# Test the function with multiple tickers
tickers = ['AAPL', 'MSFT', 'NVDA', 'TSLA', 'MS', 'GS']
returns = {}

# Store returns for each ticker
for ticker in tickers:
    data = get_price_lastweek(ticker)
    returns[ticker] = get_returns(data)
    print(f"{ticker}: {returns[ticker]:.2f}%")

# Find ticker with highest return
best_ticker = max(returns, key=returns.get)
print(f"\nHighest return was {best_ticker} at {returns[best_ticker]:.2f}%")
