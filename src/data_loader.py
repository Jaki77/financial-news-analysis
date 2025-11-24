import pandas as pd
import os
from typing import Dict

def load_price_data(folder_path: str = "./data/yfinance_data") -> Dict[str, pd.DataFrame]:
    """
    Loads all price CSVs from data/yfinance_data/
    Returns a dictionary: {ticker: DataFrame}
    """
    price_data = {}
    # expected_tickers = {'AAPL', 'AMZN', 'GOOG', 'META', 'MSFT', 'NVDA'}
    
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    print("Loading price data from:", folder_path)
    
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            ticker = file.replace(".csv", "").upper()
            # if ticker in expected_tickers:
            path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(path, parse_dates=['Date'])
                df = df.set_index('Date').sort_index()
                df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
                for col in ['Open','High','Low','Close','Volume']:
                    df[col] = df[col].astype(float)
                price_data[ticker] = df
                print(f"Success: {ticker} → {len(df)} rows | {df.index[0].date()} to {df.index[-1].date()}")
            except Exception as e:
                print(f"Failed: {ticker} → {e}")
    
    print(f"\nSuccessfully loaded {len(price_data)} stocks")
    return price_data