# src/pair_finder.py

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

    # Generate all unique combinations of tickers
    pairs_to_test = list(combinations(tickers, 2))
    print(f"Testing {len(pairs_to_test)} unique pairs...")

    for pair in pairs_to_test:
        stock1_ticker = pair[0]
        stock2_ticker = pair[1]
        
        stock1_prices = data[stock1_ticker]
        stock2_prices = data[stock2_ticker]

        # Step 1: Run an Ordinary Least Squares (OLS) regression to find the hedge ratio.
        # We regress stock2 on stock1 to find the relationship.
        # Adding a constant allows for a baseline difference in prices.
        stock1_with_const = sm.add_constant(stock1_prices)
        model = sm.OLS(stock2_prices, stock1_with_const).fit()
        hedge_ratio = model.params[stock1_ticker]

        # Step 2: Calculate the spread (the residuals of the regression).
        # The spread is the difference between the actual stock2 price and the
        # price predicted by the regression model.
        spread = stock2_prices - hedge_ratio * stock1_prices

        # Step 3: Run the Augmented Dickey-Fuller (ADF) test on the spread.
        # The null hypothesis of the ADF test is that the time series has a unit root
        # (i.e., it is non-stationary). If we can reject the null hypothesis,
        # it means the spread is stationary, and the pair is cointegrated.
        adf_result = adfuller(spread)
        p_value = adf_result[1] # The p-value is the second element of the result tuple.

        # If the p-value is below our threshold, we consider the pair cointegrated.
        if p_value < p_value_threshold:
            print(f"  >> Found cointegrated pair: {stock1_ticker} and {stock2_ticker} (p-value: {p_value:.4f})")
            cointegrated_pairs.append((stock1_ticker, stock2_ticker, p_value, hedge_ratio))

    # Sort the pairs by their p-value in ascending order (most significant first)
    cointegrated_pairs.sort(key=lambda x: x[2])
    
    return cointegrated_pairs