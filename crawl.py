import sys
import yfinance as yf
from utils import *


def main(args):
	stocks = args
	stocks.pop(0)
	if len(args) == 0:
		print("running in filter mode")
		stocks = get_stocks("nikkei.csv")
		# stocks.extend(get_stocks("sp500.csv"))
		# stocks.extend(get_stocks("asx.csv"))
		# stocks.extend(get_stocks("ftse100.csv"))
	n = len(stocks)
	print(f"	mc	pe	pb	div	div5	beta	debttoequity	profitmargin	cashpershare	earningsgrowth	revenuegrowth	name")
	tickers = yf.Tickers(stocks)
	all_pe = []
	all_div_five_year = []
	all_beta = []
	all_pb = []
	for stock in tickers.tickers:
		info = tickers.tickers[stock].info
		stock_data = parse_stock(info)
		all_beta.append(stock_data["beta"])
		all_pe.append(stock_data["pe"])
		all_pb.append(stock_data["pb"])
		if stock_data["div_five_year"] != 0:
			all_div_five_year.append(stock_data["div_five_year"])
		else:
			all_div_five_year.append(stock_data["div"])
		# if pe > 0 and pe < 30 and profit_margin >= 0.10:
		output = f"{stock}	{stock_data['market_cap']}	{stock_data['pe']}	{stock_data['pb']}	{stock_data['div']}	" \
				f"{stock_data['div_five_year']}	{stock_data['beta']}	{stock_data['debt_to_equity']}		{stock_data['profit_margin']}		"\
		f"{stock_data['cash_per_share']}		{stock_data['earnings_growth']}		{stock_data['revenue_growth']}	{stock_data['name']}"
		print(output)
	print(f"pe: {round(sum(all_pe)/n, 2)}")
	print(f"pb: {round(sum(all_pb)/n, 2)}")
	print(f"div5: {round(sum(all_div_five_year)/n, 2)}")
	print(f"beta: {round(sum(all_beta)/n, 2)}")
	print(f"stocks: {n}")

if __name__ == "__main__":
    main(sys.argv)
