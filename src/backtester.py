# src/backtester.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_backtest(data, pair_info):
    """
    Runs a backtest for a given cointegrated pair.

    Args:
        data (pd.DataFrame): DataFrame with historical price data.
        pair_info (tuple): Tuple containing pair tickers, p-value, and hedge ratio.

    Returns:
        pd.DataFrame: A DataFrame containing the portfolio performance over time.
    """
    stock1_ticker, stock2_ticker, _, hedge_ratio = pair_info
    
    print(f"\n--- Running Backtest for {stock1_ticker} and {stock2_ticker} ---")

    # --- 1. Prepare Data and Signals ---
    df = pd.DataFrame(index=data.index)
    df['s1_price'] = data[stock1_ticker]
    df['s2_price'] = data[stock2_ticker]
    
    # The spread is calculated based on the hedge ratio found during the cointegration test
    df['spread'] = df['s2_price'] - hedge_ratio * df['s1_price']
    
    # Calculate the z-score of the spread
    window = 30
    df['moving_avg'] = df['spread'].rolling(window=window).mean()
    df['moving_std'] = df['spread'].rolling(window=window).std()
    df['z_score'] = (df['spread'] - df['moving_avg']) / df['moving_std']

    # Define trading signal thresholds
    entry_threshold = 2.0
    exit_threshold = 0.5
    stop_loss_threshold = 3.0 # Risk Management: Stop-Loss

    # --- 2. Generate Positions ---
    # -1: Short the spread (Short S2, Long S1)
    # +1: Long the spread (Long S2, Short S1)
    #  0: No position
    df['position'] = 0
    in_position = False

    for i in range(1, len(df)):
        # Entry condition: Short the spread
        if not in_position and df['z_score'].iloc[i-1] > entry_threshold:
            df.loc[df.index[i], 'position'] = -1
            in_position = True
        # Entry condition: Long the spread
        elif not in_position and df['z_score'].iloc[i-1] < -entry_threshold:
            df.loc[df.index[i], 'position'] = 1
            in_position = True
        # Exit condition or Stop-Loss
        elif in_position:
            current_pos = df['position'].iloc[i-1]
            z_score = df['z_score'].iloc[i-1]
            
            # Exit a short position
            if current_pos == -1 and (z_score < exit_threshold or z_score > stop_loss_threshold):
                in_position = False
            # Exit a long position
            elif current_pos == 1 and (z_score > -exit_threshold or z_score < -stop_loss_threshold):
                in_position = False
            # Otherwise, hold the position
            else:
                df.loc[df.index[i], 'position'] = current_pos
    
    # --- 3. Calculate Portfolio Performance ---
    # Calculate daily returns of the strategy
    # Note: This is a simplified returns calculation. A more detailed one would account for transaction costs.
    df['strategy_returns'] = (df['position'].shift(1) * (hedge_ratio * df['s1_price'].pct_change() - df['s2_price'].pct_change())).fillna(0)
    
    # Calculate cumulative returns
    df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()

    return df