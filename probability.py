import yfinance as yf
import statistics
from scipy.stats import norm
import argparse
import numpy as np

# Set up argument parsing for the stock ticker
parser = argparse.ArgumentParser(description='Calculate stock statistics and tail event probabilities.')
parser.add_argument('stock', type=str, help='Stock ticker symbol (e.g., AAPL, MOAT.AX)')
args = parser.parse_args()

# Define the stock symbol from CLI arguments and other data parameters
stock = args.stock
DATA_PERIOD = '5y'  # You can adjust the period as needed (e.g., '6mo', '1y', '5d', etc.)
DATA_PERIOD_NUMERICAL = 5  # Numerical period for CAGR calculation (in years)
DATA_INTERVAL = '1mo'  # Monthly data
ADJ_CLOSE = 'Adj Close'
DATA_OFFSET = 12  # Number of periods for percent change (e.g., 12 for annualized change over 12 months)

# Download the stock data
data = yf.download(stock, period=DATA_PERIOD, interval=DATA_INTERVAL)
# ticker = yf.Tickers(stock)
# info = ticker.tickers[stock].info

# Extract the Adjusted Close prices
individual_prices = data[ADJ_CLOSE]

# Calculate percentage changes over the specified period
# price_changes = individual_prices.pct_change(periods=DATA_OFFSET).tolist()
# Calculate log returns over the specified period (12 months)
log_returns = np.log(individual_prices / individual_prices.shift(DATA_OFFSET))
log_returns = log_returns.dropna()

# Remove any NaN values from the list
# price_changes = [x for x in price_changes if str(x) != 'nan']

# Calculate statistics: mean and standard deviation (Sigma)
mean_price_change = statistics.mean(log_returns)
sigma = statistics.stdev(log_returns)

# Assuming a risk-free rate of 0.01 for simplicity in the Sharpe ratio calculation
risk_free_rate = 0.01
sharpe_ratio = (mean_price_change - risk_free_rate) / sigma if sigma != 0 else 0

# Calculate Z-scores and tail event probabilities
z_scores = [1, 2, 3]
tail_event_probabilities = [1 - norm.cdf(z) for z in z_scores]  # Probabilities of events beyond each sigma

# Calculate the magnitude of the move for each sigma level
magnitude_of_moves = [(mean_price_change - z * sigma, mean_price_change + z * sigma) for z in z_scores]

# Output the results, rounding to 2 decimals and displaying as percentages
print(f"Mean: {round(mean_price_change * 100, 2)}%")
print(f"Sigma: {round(sigma * 100, 2)}%")
print(f"Sharpe: {round(sharpe_ratio, 2)}")
# print(f"Beta: {info['beta3Year']}")

# Display only downside moves and probabilities in a list format
for i, z in enumerate(z_scores):
    lower_move = magnitude_of_moves[i][0]  # Only the downside move (lower bound)
    prob = tail_event_probabilities[i] * 100  # Probability in percentage
    print(f"{z} Sigma: Magnitude: {round(lower_move * 100, 2)}%, Probability: {round(prob, 2)}%")

# print(f"FiveYearAverage: {round(info['fiveYearAverageReturn'] * 100, 2)}")
