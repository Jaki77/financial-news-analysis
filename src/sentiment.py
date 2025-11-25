import pandas as pd
import warnings
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon', quiet=True)
warnings.filterwarnings("ignore")

sia = SentimentIntensityAnalyzer()

def analyze_sentiment_vader(headline: str) -> float:
    """VADER score: -1 (neg) to +1 (pos) – better for finance"""
    if not isinstance(headline, str) or not headline.strip():
        return 0.0
    return sia.polarity_scores(headline)['compound']

def analyze_sentiment_textblob(headline: str) -> float:
    """TextBlob polarity: for comparison"""
    if not isinstance(headline, str) or not headline.strip():
        return 0.0
    return TextBlob(headline).sentiment.polarity

def process_news_sentiment(news_path: str = "./data/newsData/raw_analyst_ratings.csv") -> pd.DataFrame:
    print("Loading FNSPID dataset...")
    news = pd.read_csv(news_path, low_memory=False)
    news.columns = [col.strip().lower() for col in news.columns]
    
    # Parse date
    # news['date'] = pd.to_datetime(news['date'], utc=True, errors='coerce')
    # news = news.dropna(subset=['date'])
    news['date'] = pd.to_datetime(news['date'], format='ISO8601', utc=True, errors='coerce')    # Force UTC first
    news['date'] = news['date'].dt.tz_convert('UTC').dt.tz_localize(None)     # Remove timezone
    news['date'] = news['date'].dt.floor('D')  
    
    # Align to trading day (as per demo: simple floor, but with after-hours shift)
    news['publication_hour_utc'] = news['date'].dt.hour
    news['is_after_close'] = news['publication_hour_utc'] >= 20  # 4 PM ET
    news['trading_day'] = news['date'].dt.floor('D')
    news.loc[news['is_after_close'], 'trading_day'] += pd.Timedelta(days=1)
    
    # Clean
    news['stock'] = news['stock'].str.upper().str.strip()
    news['headline'] = news['headline'].astype(str).str.strip()
    
    # Filter 4 stocks
    tickers = {"AAPL", "AMZN", "GOOG", "NVDA"}
    news = news[news['stock'].isin(tickers)]
    
    # Sentiment (VADER main, TextBlob secondary – as in demo)
    print("Computing sentiments...")
    news['vader_sentiment'] = news['headline'].apply(analyze_sentiment_vader)
    news['textblob_sentiment'] = news['headline'].apply(analyze_sentiment_textblob)
    
    # Aggregate daily (mean as in demo)
    daily = news.groupby(['trading_day', 'stock']).agg({
        'vader_sentiment': 'mean',
        'textblob_sentiment': 'mean'
    }).reset_index()
    
    print(f"Processed {len(daily)} daily observations")
    return daily