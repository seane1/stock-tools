import csv
import yfinance as yf
import statistics


USD = 1.51
JPY = 0.01
GBP = 1.92
EUR = 1.64
DATA_PERIOD = "5y"
DATA_INTERVAL = "1mo"
DATA_OFFSET = 12
CLOSE = "Close"
ADJ_CLOSE = "Adj Close"


def get_stocks(csv_file):
	stocks = []
	with open(csv_file, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for stock in reader:
			stocks.append(stock[0])
	return stocks


def get_prices(stocks):
    tickers = yf.Tickers(stocks)
    prices = []
    epsvals = []
    pevals = []
    betas = []
    for stock in tickers.tickers:
        info = tickers.tickers[stock].info
        keys = info.keys()
        currency = info["currency"] if "currency" in keys else 0
        price = round(convert_currency(info["currentPrice"], currency), 2) if "currentPrice" in keys else 0
        beta = info["beta"] if "beta" in keys else 0
        eps = info["trailingEps"] if "trailingEps" in keys else 0
        pe = round(info["trailingPE"], 2) if "trailingPE" in keys and type(info["trailingPE"]) is not str  else 0
        prices.append(price)
        epsvals.append(eps)
        pevals.append(pe)
        betas.append(beta)
    return prices, epsvals, pevals, betas


def get_stats(stocks):
    data = yf.download(stocks, period=DATA_PERIOD, interval=DATA_INTERVAL)
    individual_prices = data[ADJ_CLOSE]
    mus = []
    sigmas = []
    for stock in stocks:
        if len(stocks) == 1:
            prices = individual_prices.pct_change(periods=DATA_OFFSET).tolist()
        else:
            prices = individual_prices[stock].pct_change(periods=DATA_OFFSET).tolist()
        prices = [x for x in prices if str(x) != 'nan']
        n = len(prices)
        total = sum(prices)
        mu = round(total/n, 3)
        sigma = round(statistics.stdev(prices), 3)
        mus.append(mu)
        sigmas.append(sigma)
    prices, eps, pes, betas = get_prices(stocks)
    return list(zip(stocks, prices, mus, sigmas, eps, pes, betas))


def convert_currency(field, currency):
	if currency == "USD":
		field = field * USD
	elif currency == "JPY":
		field = field * JPY
	elif currency == "GBP":
		field = field * GBP
	elif currency == "EUR":
		field = field * EUR
	return field
