import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.correlation import correlation_analysis

if __name__ == "__main__":
    print("TASK 3: NEWS SENTIMENT → STOCK RETURNS CORRELATION")
    print("For AAPL, AMZN, GOOG, NVDA\n")
    
    results = correlation_analysis()
    
    print("\nTASK 3 COMPLETE!")
    print("Now open notebook correlation_analysis.ipynb for visualization")