import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from itertools import combinations

def find_cointegrated_pairs(data, p_value_threshold):
    """
    Finds cointegrated pairs of stocks from a DataFrame of prices.

    Args:
        data (pd.DataFrame): DataFrame with stock prices, where columns are tickers.
        p_value_threshold (float): The significance level for the cointegration test.

    Returns:
        list: A list of tuples, where each tuple contains the pair of tickers,
              the p-value of the cointegration test, and the hedge ratio.
    """
    n_stocks = data.shape[1]
    tickers = data.columns
    cointegrated_pairs = []

    print(f"Searching for cointegrated pairs among {n_stocks} stocks...")

    pairs_to_test = list(combinations(tickers, 2))
    print(f"Testing {len(pairs_to_test)} unique pairs...")

    for pair in pairs_to_test:
        stock1_ticker = pair[0]
        stock2_ticker = pair[1]
        
        stock1_prices = data[stock1_ticker]
        stock2_prices = data[stock2_ticker]

        stock1_with_const = sm.add_constant(stock1_prices)
        model = sm.OLS(stock2_prices, stock1_with_const).fit()
        hedge_ratio = model.params[stock1_ticker]


        spread = stock2_prices - hedge_ratio * stock1_prices


        adf_result = adfuller(spread)
        p_value = adf_result[1]

        if p_value < p_value_threshold:
            print(f"  >> Found cointegrated pair: {stock1_ticker} and {stock2_ticker} (p-value: {p_value:.4f})")
            cointegrated_pairs.append((stock1_ticker, stock2_ticker, p_value, hedge_ratio))

    cointegrated_pairs.sort(key=lambda x: x[2])
    
    return cointegrated_pairs
