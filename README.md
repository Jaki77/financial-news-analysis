# 10 Academy: Artificial Intelligence Mastery  
## Week 1 Challenge – Predicting Price Moves with News Sentiment  
**Nova Financial Solutions**  
**Date**: 19 – 25 Nov 2025  
**Author**: Jaki77  

### Business Objective
Help Nova Financial enhance its predictive analytics capabilities by discovering and quantifying the relationship between financial news headline sentiment and daily stock price movements using the FNSPID dataset.

### Project Status (as of 24 Nov 2025)
| Task | Status       | Notes |
|------|--------------|-------|
| Task 1: Git & GitHub + EDA + Text Analysis | Complete | Professional structure, full EDA, n-grams, topic modeling |
| Task 2: Quantitative Analysis (TA-Lib + yfinance) | In Progress | Modular code, all indicators |
| Task 3: Sentiment vs Returns Correlation | In Progress | Final step – merging sentiment with daily returns |


### Repository Structure
├── data/
│   ├── yfinance_data/               ← Raw price data
│   └── newsData                     ← Raw news data
├── src/
│   ├── data_loader.py               ← Dedicated price data ingestion
│   ├── technical_indicators.py      ← TA-Lib calculations
│   └── sentiment.py                 ← (Task 3 – coming soon)
├── scripts/
│   └── compute_technical_indicators.py  ← Production script
├── notebooks/
│   ├── eda.ipynb
│   └── quantitative_analysis.ipynb
├── requirements.txt
└── README.md

### How to Run
```bash
# 1. Clone and enter repo
git clone https://github.com/Jaki77/financial-news-analysis.git
cd financial-news-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Compute technical indicators (one-time)
python scripts/compute_technical_indicators.py

# 4. Open notebooks
jupyter notebook