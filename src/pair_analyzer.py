import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyze_and_plot_pair(data, pair):
    """
    Analyzes a given pair of stocks and plots their price ratio, moving average,
    and trading bands (z-score).

    Args:
        data (pd.DataFrame): DataFrame containing the price data for all stocks.
        pair (tuple): A tuple containing the tickers of the two stocks in the pair.
    """
    stock1_ticker, stock2_ticker = pair[0], pair[1]
    
    print(f"\nAnalyzing and plotting pair: {stock1_ticker} vs {stock2_ticker}")

    price_ratio = data[stock1_ticker] / data[stock2_ticker]

    window = 30
    moving_avg = price_ratio.rolling(window=window, center=False).mean()
    moving_std = price_ratio.rolling(window=window, center=False).std()

    z_score = (price_ratio - moving_avg) / moving_std

    plt.style.use('seaborn-v0_8-darkgrid')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True,
                                   gridspec_kw={'height_ratios': [2, 1]})
    
    fig.suptitle(f'Pairs Trading Analysis: {stock1_ticker} and {stock2_ticker}', fontsize=16)

    ax1.plot(price_ratio.index, price_ratio, label='Price Ratio (S1/S2)', color='royalblue', lw=1.5)
    ax1.plot(moving_avg.index, moving_avg, label=f'{window}-Day Moving Avg', color='darkorange', lw=2, linestyle='--')
    
    ax1.fill_between(moving_avg.index, moving_avg - 2*moving_std, moving_avg + 2*moving_std,
                     color='gray', alpha=0.2, label='+/- 2 Std Dev')
    ax1.fill_between(moving_avg.index, moving_avg - moving_std, moving_avg + moving_std,
                     color='gray', alpha=0.3, label='+/- 1 Std Dev')

    ax1.set_title('Price Ratio and Bollinger Bands')
    ax1.set_ylabel('Ratio')
    ax1.legend()
    ax1.grid(True)

    ax2.plot(z_score.index, z_score, label='Z-Score', color='forestgreen', lw=1.5)
    
    ax2.axhline(2.0, color='red', linestyle='--', lw=1, label='Sell Signal (Short S1, Long S2)')
    ax2.axhline(1.0, color='red', linestyle=':', lw=1)
    ax2.axhline(0.0, color='black', linestyle='--', lw=1)
    ax2.axhline(-1.0, color='green', linestyle=':', lw=1)
    ax2.axhline(-2.0, color='green', linestyle='--', lw=1, label='Buy Signal (Long S1, Short S2)')

    ax2.set_title('Z-Score of Price Ratio')
    ax2.set_ylabel('Z-Score')
    ax2.set_xlabel('Date')
    ax2.legend(loc='upper left')
    ax2.grid(True)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
