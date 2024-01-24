import csv
import yfinance as yf

BILLION = 1000000000

def get_stocks(csv_file):
	stocks = []
	with open(csv_file, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for stock in reader:
			stocks.append(stock[0])
	return stocks


def main():
	print("stock	pe	mc	div	beta	debttoequity	profitmargin	cashpershare	earningsgrowth	revenuegrowth")

	stocks = get_stocks("asx.csv")
	stocks.extend(get_stocks("sp500.csv"))
	stocks.extend(get_stocks("nikkei.csv"))

	tickers = yf.Tickers(stocks)
	for stock in tickers.tickers:
		info = tickers.tickers[stock].info
		keys = info.keys()
		price = info["currentPrice"] if "currentPrice" in keys else 0
		eps = info["trailingEps"] if "trailingEps" in keys else 0
		pe = round(info["trailingPE"], 2) if "trailingPE" in keys and type(info["trailingPE"]) is not str  else 0
		beta = info["beta"] if "beta" in keys else 0
		debt_to_equity = round(info["debtToEquity"]/100, 2) if "debtToEquity" in keys else 0
		market_cap = int(info["marketCap"]/BILLION) if "marketCap" in keys else 0
		profit_margin = round(info["profitMargins"], 2) if "profitMargins" in keys else 0
		cash_per_share = round(info["totalCashPerShare"], 2) if "totalCashPerShare" in keys else 0
		earnings_growth = info["earningsGrowth"] if "earningsGrowth" in keys else 0
		revenue_growth = info["revenueGrowth"] if "revenueGrowth" in keys else 0
		div_unconverted = info.get("trailingAnnualDividendYield")
		div = round(div_unconverted * 100, 2) if div_unconverted is not None else 0
		if pe > 0 and pe < 25 and market_cap > 1:
			print(f"{stock}	{pe}	{market_cap}	{div}	{beta}	{debt_to_equity}		{profit_margin}		{cash_per_share}		{earnings_growth}		{revenue_growth}")

if __name__ == "__main__":
    main()
