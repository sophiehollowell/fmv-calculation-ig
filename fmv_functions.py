## import necessary packages
import yfinance as yf
from datetime import datetime, timedelta

## functions
def get_next_trading_day(date, ticker):
    """
    Returns the first trading day on or after 'date' for the given ticker.
    """
    stock = yf.Ticker(ticker)
    while True:
        next_day = date + timedelta(days=1)
        hist = stock.history(start=date.strftime("%Y-%m-%d"), end=next_day.strftime("%Y-%m-%d"))
        if not hist.empty:
            return date, hist  # Found the trading day
        date += timedelta(days=1)  # Move forward one day and try again

def get_fmv(ticker: str, date_str: str):
    """
    Returns the FMV for the first trading day on or after the given date.
    """
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        date, hist = get_next_trading_day(date, ticker)

        high = hist["High"].iloc[0]
        low = hist["Low"].iloc[0]
        fmv = (high + low) / 2

        return {
            "ticker": ticker.upper(),
            "date_used": date.strftime("%Y-%m-%d"),
            "high": round(high, 2),
            "low": round(low, 2),
            "fmv": round(fmv, 2)
        }

    except Exception as e:
        print(f"Error fetching data for {ticker} on {date_str}: {e}")
        return None