import sys
from utils import *


def main(args):
    stocks = args
    stocks.pop(0)
    if len(args) == 0:
        print("running in filter mode")
        stocks = get_stocks("nikkei.csv")
        # stocks.extend(get_stocks("sp500.csv"))
        # stocks.extend(get_stocks("asx.csv"))
    stock_list = get_stats(stocks)
    # filtered_stocks = [x for x in stock_list if x[2] >= 0.10]
    returns = []
    sigmas = []
    betas = []
    print(f"            price  mean   sigma   beta")
    for stock in stock_list:
        code = stock[0]
        price = stock[1]
        gain = stock[2]
        sigma_individual = stock[3]
        beta_individual = stock[6]
        returns.append(gain)
        betas.append(beta_individual)
        sigmas.append(sigma_individual)
        print(f"{code}          {price}  {gain}     {sigma_individual}   {beta_individual}")
    n = len(returns)
    total = sum(returns)
    mu = round(total / n, 2)
    beta = round(sum(betas) / n, 2)
    sigma = round(sum(sigmas) / n, 2)
    print(f"{mu}    {sigma}    {beta}")


if __name__ == "__main__":
    main(sys.argv)
