import yfinance as yf
import pandas as pd
import os

def fetch_data(tickers, start_date, end_date, file_path):
    """
    Downloads historical 'Adj Close' prices for a list of tickers and saves them to a CSV file.

    Args:
        tickers (list): A list of stock ticker symbols.
        start_date (str): The start date for the data in 'YYYY-MM-DD' format.
        end_date (str): The end date for the data in 'YYYY-MM-DD' format.
        file_path (str): The path to save the resulting CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the 'Adj Close' prices for the tickers.
                      Returns None if data fetching fails.
    """
    print(f"Fetching data for {len(tickers)} tickers from {start_date} to {end_date}...")
    
    try:
        data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)
        
        if data.empty:
            print("Error: No data downloaded. Check tickers and date range.")
            return None
            
        adj_close_prices = data['Adj Close']
        
        adj_close_prices.dropna(axis=1, how='all', inplace=True)
        
        adj_close_prices.dropna(axis=0, how='any', inplace=True)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        adj_close_prices.to_csv(file_path)
        print(f"Data successfully saved to {file_path}")
        
        return adj_close_prices
        
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return None
