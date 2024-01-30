import csv
import sys
import yfinance as yf
# from datetime import datetime
# import pandas_datareader as web

BILLION = 1000000000
USD = 1.51

def get_stocks(csv_file):
	stocks = []
	with open(csv_file, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for stock in reader:
			stocks.append(stock[0])
	return stocks


def main(args):
	# stocks = get_stocks("asx.csv")
	# stocks.extend(get_stocks("sp500.csv"))
	# stocks.extend(get_stocks("nikkei.csv"))
	# stocks.extend(get_stocks("ftse100.csv"))

	# stocks = ["RIO.AX", "BHP.AX", "STO.AX", "WDS.AX", "ALL.AX", "SHL.AX", "MO", "XOM"]

	stocks = args
	stocks.pop(0)
	n = len(stocks)

	print(f"	pe	mc	div	div5	beta	debttoequity	profitmargin	cashpershare	earningsgrowth	revenuegrowth")

	tickers = yf.Tickers(stocks)
	all_pe = []
	all_div_five_year = []
	all_beta = []
	# multpl_stocks = web.get_data_yahoo(stocks, start = "2014-01-01", end = datetime.now().strftime("%Y-%m-%d"))
	for stock in tickers.tickers:
		info = tickers.tickers[stock].info
		keys = info.keys()
		price = info["currentPrice"] if "currentPrice" in keys else 0
		eps = info["trailingEps"] if "trailingEps" in keys else 0
		pe = round(info["trailingPE"], 2) if "trailingPE" in keys and type(info["trailingPE"]) is not str  else 0
		all_pe.append(pe)
		beta = info["beta"] if "beta" in keys else 0
		all_beta.append(beta)
		debt_to_equity = round(info["debtToEquity"]/100, 2) if "debtToEquity" in keys else 0
		market_cap = int(info["marketCap"]/BILLION) if "marketCap" in keys else 0
		currency = info["currency"] if "currency" in keys else 0
		if currency != 0 and currency == "USD":
			market_cap = int(market_cap * USD)
		profit_margin = round(info["profitMargins"], 2) if "profitMargins" in keys else 0
		cash_per_share = round(info["totalCashPerShare"], 2) if "totalCashPerShare" in keys else 0
		earnings_growth = info["earningsGrowth"] if "earningsGrowth" in keys else 0
		revenue_growth = info["revenueGrowth"] if "revenueGrowth" in keys else 0
		div_unconverted = info.get("trailingAnnualDividendYield")
		div_five_year = info["fiveYearAvgDividendYield"] if "fiveYearAvgDividendYield" in keys else 0
		div = round(div_unconverted * 100, 2) if div_unconverted is not None else 0
		if div_five_year != 0:
			all_div_five_year.append(div_five_year)
		else:
			all_div_five_year.append(div)
		# if pe > 0 and pe < 25 and market_cap > 1:
		print(f"{stock}	{pe}	{market_cap}	{div}	{div_five_year}	{beta}	{debt_to_equity}		{profit_margin}		{cash_per_share}		{earnings_growth}		{revenue_growth}")
	print(f"pe: {round(sum(all_pe)/n, 2)}")
	print(f"div5: {round(sum(all_div_five_year)/n, 2)}")
	print(f"beta: {round(sum(all_beta)/n, 2)}")
	print(f"stocks: {n}")

if __name__ == "__main__":
    main(sys.argv)
