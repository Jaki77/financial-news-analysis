import sys
import os
import talib
from typing import Dict
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.data_loader import load_price_data

def add_ta_indicators(df: pd.DataFrame) -> pd.DataFrame:
    close = df['Close'].values
    high = df['High'].values
    low = df['Low'].values
    volume = df['Volume'].values

    df = df.copy()
    df['SMA_20'] = talib.SMA(close, timeperiod=20)
    df['SMA_50'] = talib.SMA(close, timeperiod=50)
    df['EMA_12'] = talib.EMA(close, timeperiod=12)
    df['EMA_26'] = talib.EMA(close, timeperiod=26)
    df['RSI_14'] = talib.RSI(close, timeperiod=14)
    df['MACD'], df['MACD_signal'], df['MACD_hist'] = talib.MACD(close)
    df['BB_upper'], df['BB_middle'], df['BB_lower'] = talib.BBANDS(close)
    df['ATR_14'] = talib.ATR(high, low, close, timeperiod=14)
    df['Vol_SMA_20'] = talib.SMA(volume, timeperiod=20)
    
    return df

def process_all_stocks() -> Dict[str, pd.DataFrame]:
    data = load_price_data()  # uses default path
    for ticker, df in data.items():
        data[ticker] = add_ta_indicators(df)
    return data