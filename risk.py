import sys
from utils import *


def main(args):
    stocks = args
    stocks.pop(0)
    if len(args) == 0:
        print("running in filter mode")
        stocks = get_stocks("nikkei.csv")
        # stocks.extend(get_stocks("asx.csv"))
        # stocks.extend(get_stocks("sp500.csv"))
    stock_list = get_stats(stocks)
    # update_db(stock_list)
    # filtered_stocks = [x for x in stock_list if x[2] >= 0.10]
    means = []
    sigmas = []
    betas = []
    annual_returns = []
    pes = []
    sharpes = []
    print(f"\treturn\tmean\tsigma\tsharpe\tbeta\tpe\tbuy\tname")
    for stock in stock_list:
        code = stock[0]
        price = stock[1]
        mean = stock[2]
        sigma_individual = stock[3]
        pe = stock[5]
        beta_individual = stock[6]
        annual_return = stock[7]
        div_five = stock[8]
        name = stock[9]
        sharpe = stock[10]
        combined_return = annual_return + div_five
        sharpes.append(sharpe)
        means.append(mean)
        betas.append(beta_individual)
        sigmas.append(sigma_individual)
        annual_returns.append(combined_return)
        pes.append(pe)
        # if sharpe >= 0.7:
        print(f"{code}\t{'%.2f' % combined_return}\t{mean}\t{sigma_individual}\t{sharpe}\t{beta_individual}\t{pe}\t{round(price*100)}\t{name}")
    n = len(means)
    total = sum(means)
    mu = round(total / n, 2)
    beta = round(sum(betas) / n, 2)
    sigma = round(sum(sigmas) / n, 2)
    average_return = round(sum(annual_returns) / n, 2)
    pe = round(sum(pes) / n, 2)
    sharpe = round(sum(sharpes) / n, 2)
    print()
    print(f"mu:\t{mu}")
    print(f"sigma:\t{sigma}")
    print(f"beta:\t{beta}")
    print(f"return:\t{average_return}")
    print(f"sharpe:\t{sharpe}")
    print(f"pe:\t{pe}")


if __name__ == "__main__":
    main(sys.argv)
