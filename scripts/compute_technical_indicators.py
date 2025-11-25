import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.technical_indicators import process_all_stocks
import pickle
if __name__ == "__main__":
    print("Computing technical indicators...\n")
    price_data = process_all_stocks()
    
    save_path = "./data/processed_price_data_with_indicators.pkl"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    with open(save_path, "wb") as f:
        pickle.dump(price_data, f)
    
    print(f"\nAll done! Saved to: \n{save_path}")
    print("Run the notebook now: quantitative_analysis.ipynb")