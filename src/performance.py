# src/performance.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_performance_metrics(portfolio_df):
    """
    Calculates key performance metrics from a portfolio DataFrame.

    Args:
        portfolio_df (pd.DataFrame): DataFrame with strategy returns.

    Returns:
        dict: A dictionary containing performance metrics.
    """
    metrics = {}
    
    # Total Cumulative Return
    total_return = portfolio_df['cumulative_returns'].iloc[-1] - 1
    metrics['Total Return'] = f"{total_return:.2%}"
    
    # Annualized Return
    days = (portfolio_df.index[-1] - portfolio_df.index[0]).days
    annualized_return = (1 + total_return) ** (365.0 / days) - 1
    metrics['Annualized Return'] = f"{annualized_return:.2%}"

    # Annualized Volatility
    annualized_volatility = portfolio_df['strategy_returns'].std() * np.sqrt(252)
    metrics['Annualized Volatility'] = f"{annualized_volatility:.2%}"

    # Sharpe Ratio (assuming risk-free rate is 0)
    sharpe_ratio = annualized_return / annualized_volatility if annualized_volatility != 0 else 0
    metrics['Sharpe Ratio'] = f"{sharpe_ratio:.2f}"

    # Maximum Drawdown
    cumulative_returns = portfolio_df['cumulative_returns']
    running_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - running_max) / running_max
    max_drawdown = drawdown.min()
    metrics['Maximum Drawdown'] = f"{max_drawdown:.2%}"

    return metrics

def plot_performance(portfolio_df, pair_info):
    """
    Plots the equity curve and z-score for the backtest.
    """
    stock1_ticker, stock2_ticker, _, _ = pair_info
    
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), sharex=True,
                                   gridspec_kw={'height_ratios': [2, 1]})
    
    fig.suptitle(f'Backtest Performance: {stock1_ticker} and {stock2_ticker}', fontsize=16)

    # Plot 1: Equity Curve
    ax1.plot(portfolio_df['cumulative_returns'], label='Strategy Cumulative Returns', color='royalblue', lw=2)
    ax1.set_title('Equity Curve')
    ax1.set_ylabel('Cumulative Returns')
    ax1.legend()
    ax1.grid(True)

    # Plot 2: Z-Score with Trades
    ax2.plot(portfolio_df['z_score'], label='Z-Score', color='forestgreen', lw=1.5)
    ax2.axhline(2.0, color='red', linestyle='--', lw=1)
    ax2.axhline(-2.0, color='green', linestyle='--', lw=1)
    ax2.axhline(0.0, color='black', linestyle=':', lw=1)
    
    # Overlay trade entry/exit points
    long_signals = portfolio_df[portfolio_df['position'] == 1].index
    short_signals = portfolio_df[portfolio_df['position'] == -1].index
    
    ax2.plot(long_signals, portfolio_df.loc[long_signals]['z_score'], '^', markersize=8, color='g', label='Long Spread')
    ax2.plot(short_signals, portfolio_df.loc[short_signals]['z_score'], 'v', markersize=8, color='r', label='Short Spread')

    ax2.set_title('Z-Score and Trading Signals')
    ax2.set_ylabel('Z-Score')
    ax2.set_xlabel('Date')
    ax2.legend(loc='upper left')
    ax2.grid(True)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()