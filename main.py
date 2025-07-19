# main.py

import pandas as pd
import os

# Import project-specific modules and configurations
from src import config
from src.data_fetcher import fetch_data
from src.pair_finder import find_cointegrated_pairs
from src.pair_analyzer import analyze_and_plot_pair
from src.backtester import run_backtest
from src.performance import calculate_performance_metrics, plot_performance

def run_analysis():
    """
    Main function to execute the pairs trading analysis pipeline.
    """
    print("--- Starting Statistical Arbitrage Analysis ---")

    # --- Step 1: Fetch or Load Data ---
    if not os.path.exists(config.DATA_FILE_PATH):
        print(f"Data file not found at '{config.DATA_FILE_PATH}'.")
        stock_data = fetch_data(
            tickers=config.TICKERS,
            start_date=config.START_DATE,
            end_date=config.END_DATE,
            file_path=config.DATA_FILE_PATH
        )
    else:
        print(f"Loading existing data from '{config.DATA_FILE_PATH}'.")
        stock_data = pd.read_csv(config.DATA_FILE_PATH, index_col='Date', parse_dates=True)

    if stock_data is None or stock_data.empty:
        print("Failed to load data. Exiting.")
        return

    # --- Step 2: Find Cointegrated Pairs ---
    cointegrated_pairs = find_cointegrated_pairs(
        data=stock_data,
        p_value_threshold=config.P_VALUE_THRESHOLD
    )

    # --- Step 3: Analyze, Backtest, and Report Results ---
    if not cointegrated_pairs:
        print("\n--- Analysis Complete ---")
        print("No cointegrated pairs found with the given parameters.")
    else:
        print(f"\n--- Analysis Complete: Found {len(cointegrated_pairs)} Cointegrated Pair(s) ---")
        
        # --- Analyze and plot the best pair ---
        best_pair_info = cointegrated_pairs[0]
        analyze_and_plot_pair(data=stock_data, pair=(best_pair_info[0], best_pair_info[1]))

        # --- Run the backtest on the best pair ---
        portfolio_df = run_backtest(data=stock_data, pair_info=best_pair_info)
        
        # --- Calculate and display performance metrics ---
        metrics = calculate_performance_metrics(portfolio_df)
        print("\n--- Backtest Performance Metrics ---")
        for metric, value in metrics.items():
            print(f"  {metric}: {value}")
        
        # --- Plot the performance ---
        plot_performance(portfolio_df, best_pair_info)

    print("\n--- End of Program ---")


if __name__ == "__main__":
    run_analysis()