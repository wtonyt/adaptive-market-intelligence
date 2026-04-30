import yfinance as yf
from datetime import datetime
import os

SYMBOLS = ["AAPL", "MSFT", "NVDA", "SPY"]

def fetch_data(symbol):
    df = yf.download(symbol, period="1y")
    df.reset_index(inplace=True)
    return df

def save_data(df, symbol):
    today = datetime.today().strftime("%Y-%m-%d")
    folder = f"data/raw/{symbol}"
    os.makedirs(folder, exist_ok=True)

    path = f"{folder}/{today}.csv"
    df.to_csv(path, index=False)

    print(f"Saved {symbol} to {path}")

if __name__ == "__main__":
    for symbol in SYMBOLS:
        df = fetch_data(symbol)
        save_data(df, symbol)
