# src/config.py

# List of stock tickers to analyze for potential pairs.
# It's best to choose stocks from the same sector for a higher chance of cointegration.
# Example: A mix of large-cap tech stocks.
TICKERS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 
    'ADBE', 'CRM', 'INTC', 'CSCO', 'ORCL', 'QCOM'
]

# The date range for fetching historical stock data.
START_DATE = "2020-01-01"
END_DATE = "2023-12-31"

# The significance level (p-value) for the Augmented Dickey-Fuller (ADF) test.
# A p-value below this threshold suggests that the pair's spread is stationary,
# and therefore, they are likely cointegrated.
P_VALUE_THRESHOLD = 0.05

# Path to store the downloaded stock data.
DATA_FILE_PATH = "data/stock_prices.csv"