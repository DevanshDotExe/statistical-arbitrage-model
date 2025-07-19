# Advanced Statistical Arbitrage (Pairs Trading) Model

This project implements a quantitative trading strategy known as pairs trading. It identifies historically cointegrated pairs of stocks and simulates a trading strategy based on the principle of mean reversion. When the price ratio of a cointegrated pair diverges significantly from its historical mean, the strategy initiates a trade: shorting the outperforming stock and going long on the underperforming one, betting that the spread will revert to its average.

This repository contains the complete Python code for data fetching, statistical analysis, backtesting, and performance evaluation.

---

## Features

- **Data Fetching**: Downloads historical stock price data from Yahoo Finance for a given list of tickers and date range.
- **Cointegration Analysis**: Systematically tests all possible pairs of stocks for cointegration using the Augmented Dickey-Fuller (ADF) test to find statistically significant relationships.
- **Strategy Backtesting**: Implements a full backtesting engine that simulates trades based on z-score deviations from the moving average of a pair's spread.
- **Risk Management**: Includes a basic stop-loss mechanism to limit potential losses on a trade.
- **Performance Metrics**: Calculates and reports key performance metrics, including:
  - Total & Annualized Return
  - Annualized Volatility
  - Sharpe Ratio
  - Maximum Drawdown
- **Visualization**: Generates plots for pair analysis (price ratio, Bollinger Bands) and backtest performance (equity curve, trade signals).

---

## Key Technologies

- **Python**: The core programming language.
- **Pandas**: For data manipulation and analysis.
- **NumPy**: For numerical operations.
- **Statsmodels**: For statistical tests, specifically the Augmented Dickey-Fuller test.
- **yfinance**: For fetching historical stock market data.
- **Matplotlib**: For data visualization and plotting.

---

## Project Structure

The project is organized into a `src` directory containing modularized Python scripts.


statistical-arbitrage/
│
├── data/                  # Stores downloaded stock price data
│   └── stock_prices.csv
│
├── src/                   # Source code modules
│   ├── init.py
│   ├── config.py          # Main configuration (tickers, dates)
│   ├── data_fetcher.py    # Fetches data from yfinance
│   ├── pair_finder.py     # Finds cointegrated pairs
│   ├── pair_analyzer.py   # Visualizes a single pair's relationship
│   ├── backtester.py      # Runs the trading simulation
│   └── performance.py     # Calculates and plots performance
│
├── .gitignore             # Specifies files for Git to ignore
├── main.py                # Main script to run the entire pipeline
├── requirements.txt       # Lists project dependencies
└── README.md              # This file


---

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/statistical-arbitrage-model.git](https://github.com/your-username/statistical-arbitrage-model.git)
    cd statistical-arbitrage-model
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the environment
    python -m venv venv

    # Activate on macOS/Linux
    source venv/bin/activate

    # Activate on Windows
    # .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **(Optional) Customize the analysis:**
    Open `src/config.py` to change the list of `TICKERS` or the `START_DATE` and `END_DATE`.

5.  **Run the analysis:**
    Execute the main script from the root directory.
    ```bash
    python main.py
    ```
    The script will fetch data, find cointegrated pairs, print the results, and generate plots for the best pair found.
