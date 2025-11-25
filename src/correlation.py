import os
import pandas as pd
import pickle
import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau
from src.sentiment import process_news_sentiment
import matplotlib.pyplot as plt
import seaborn as sns

def compute_daily_returns(price_data: dict) -> dict:
    returns = {}
    for ticker, df in price_data.items():
        df_ret = df[['Close']].pct_change().dropna()
        df_ret.columns = ['daily_return']
        returns[ticker] = df_ret
    return returns

def correlation_analysis():
    # Load prices
    with open("./data/processed_price_data_with_indicators.pkl", "rb") as f:
        price_data = pickle.load(f)
    
    returns_data = compute_daily_returns(price_data)
    
    # Process news
    daily_sentiment = process_news_sentiment()
    
    tickers = ["AAPL", "AMZN", "GOOG", "NVDA"]
    
    all_merged = pd.DataFrame()
    results = []
    
    for ticker in tickers:
        ret_df = returns_data[ticker].copy()
        ret_df.index = pd.to_datetime(ret_df.index)
        ret_df = ret_df[['daily_return']]
        
        sent_df = daily_sentiment[daily_sentiment['stock'] == ticker].set_index('trading_day')
        
        # Align on trading day (exact merge as in demo)
        merged = ret_df.join(sent_df, how='inner').dropna()
        merged['ticker'] = ticker
        all_merged = pd.concat([all_merged, merged])
        
        if len(merged) < 20:
            continue
        
        # Multiple correlations (as in demo)
        pear_corr, pear_p = pearsonr(merged['daily_return'], merged['vader_sentiment'])
        spear_corr, spear_p = spearmanr(merged['daily_return'], merged['vader_sentiment'])
        kend_corr, kend_p = kendalltau(merged['daily_return'], merged['vader_sentiment'])
        
        results.append({
            'Ticker': ticker,
            'Valid Days': len(merged),
            'Pearson Corr': round(pear_corr, 4),
            'Pearson P': round(pear_p, 4),
            'Spearman Corr': round(spear_corr, 4),
            'Kendall Corr': round(kend_corr, 4),
            'Significant': pear_p < 0.05
        })
    
    results_df = pd.DataFrame(results).sort_values('Pearson Corr', ascending=False)
    results_df.to_csv("./data/task3_results.csv", index=False)
      
    return results_df