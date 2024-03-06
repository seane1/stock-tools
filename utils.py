import csv
import yfinance as yf
import statistics
import math
from constants import *


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
    div_fives = []
    for stock in tickers.tickers:
        info = tickers.tickers[stock].info
        stock = parse_stock(info)
        prices.append(stock["price"])
        epsvals.append(stock["eps"])
        pevals.append(stock["pe"])
        betas.append(stock["beta"])
        div_fives.append(stock["div_five_year"])
    return prices, epsvals, pevals, betas, div_fives


def get_stats(stocks):
    data = yf.download(stocks, period=DATA_PERIOD, interval=DATA_INTERVAL)
    individual_prices = data[ADJ_CLOSE]
    mus = []
    sigmas = []
    annual_returns = []
    for stock in stocks:
        if len(stocks) == 1:
            price_changes = individual_prices.pct_change(periods=DATA_OFFSET).tolist()
            prices = individual_prices.tolist()
        else:
            price_changes = individual_prices[stock].pct_change(periods=DATA_OFFSET).tolist()
            prices = individual_prices[stock].tolist()
        price_changes = [x for x in price_changes if str(x) != 'nan']
        annual_return = get_return(prices[0], prices[-1])
        n = len(price_changes)
        total = sum(price_changes)
        mu = round(round(total/n, 4) * 100, 2)
        sigma = round(round(statistics.stdev(price_changes), 4) * 100, 2)
        mus.append(mu)
        sigmas.append(sigma)
        annual_returns.append(annual_return)
    prices, eps, pes, betas, div_fives = get_prices(stocks)
    return list(zip(stocks, prices, mus, sigmas, eps, pes, betas, annual_returns, div_fives))


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


def get_return(price_start, price_end):
	return round((math.log(price_end/price_start)/DATA_PERIOD_NUMERICAL),4)*100


def parse_stock(info):
	keys = info.keys()
	market_cap = int(info["marketCap"]/BILLION) if "marketCap" in keys else 0
	currency = info["currency"] if "currency" in keys else 0
	cash_per_share = round(info["totalCashPerShare"], 2) if "totalCashPerShare" in keys else 0
	div_unconverted = info.get("trailingAnnualDividendYield")
	div = round(div_unconverted * 100, 2) if div_unconverted is not None else 0
	stock = {
        "name" : info["longName"] if "longName" in keys else "None",
        "pb" : round(info["priceToBook"], 2) if "priceToBook" in keys and type(info["priceToBook"]) is not str  else 0,
        "currency" : currency,
        "price" : round(convert_currency(info["currentPrice"], currency), 2) if "currentPrice" in keys else 0,
        "eps" : info["trailingEps"] if "trailingEps" in keys else 0,
        "pe" : round(info["trailingPE"], 2) if "trailingPE" in keys and type(info["trailingPE"]) is not str  else 0,
        "beta" : info["beta"] if "beta" in keys else 0,
        "debt_to_equity" : round(info["debtToEquity"]/100, 2) if "debtToEquity" in keys else 0,
        "market_cap" : market_cap,
        "cash_per_share" : cash_per_share,
        "market_cap" : int(convert_currency(market_cap, currency)) if currency != 0 else 0,
        "cash_per_share" : round(convert_currency(cash_per_share, currency), 2) if currency != 0 else 0,
        "profit_margin" : round(info["profitMargins"], 2) if "profitMargins" in keys else 0,
        "earnings_growth" : info["earningsGrowth"] if "earningsGrowth" in keys else 0,
        "revenue_growth" : info["revenueGrowth"] if "revenueGrowth" in keys else 0,
        "div" : div,
        "div_five_year" : info["fiveYearAvgDividendYield"] if "fiveYearAvgDividendYield" in keys else 0,
    }
	return stock
