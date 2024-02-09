import sys
import random
import time
import yfinance as yf
import statistics
from crawler import convert_currency


UNIVERSES = 100
RANGE = 10
PORTFOLIO = 10000
DATA_PERIOD = "5y"
DATA_INTERVAL = "3mo"
DATA_OFFSET = 4
CLOSE = "Close"
ADJ_CLOSE = "Adj Close"
PE_FACTOR = 2
EPS_GROWTH_RATE = 1.1


def roll():
    first = random.randint(1,6)
    second = random.randint(1,6)
    probability = first + second
    return probability


def get_prices(stocks):
    tickers = yf.Tickers(stocks)
    prices = []
    epsvals = []
    pevals = []
    for stock in tickers.tickers:
        info = tickers.tickers[stock].info
        keys = info.keys()
        currency = info["currency"] if "currency" in keys else 0
        price = round(convert_currency(info["currentPrice"], currency), 2) if "currentPrice" in keys else 0
        eps = info["trailingEps"] if "trailingEps" in keys else 0
        pe = round(info["trailingPE"], 2) if "trailingPE" in keys and type(info["trailingPE"]) is not str  else 0
        prices.append(price)
        epsvals.append(eps)
        pevals.append(pe)
    return prices, epsvals, pevals


def get_stats(stocks):
    data = yf.download(stocks, period=DATA_PERIOD, interval=DATA_INTERVAL)
    individual_prices = data[ADJ_CLOSE]
    mus = []
    sigmas = []
    for stock in stocks:
        if len(stocks) == 1:
            prices = individual_prices[0::DATA_OFFSET].pct_change().tolist()
        else:
            prices = individual_prices[stock][0::DATA_OFFSET].pct_change().tolist()
        prices = [x for x in prices if str(x) != 'nan']
        n = len(prices)
        total = sum(prices)
        mu = round(total/n, 3)
        sigma = round(statistics.stdev(prices), 3)
        mus.append(mu)
        sigmas.append(sigma)
    prices, eps, pes = get_prices(stocks)
    return list(zip(stocks, prices, mus, sigmas, eps, pes))


def simulate(stocks):
    zero_stocks = []
    zero_count = 0
    final_values = []
    # mulitple universes
    for x in range(UNIVERSES):
        final_value = 0
        for stock in stocks:
            (stockticker, price_initial, mu, sigma, eps_initial, pe_initial) = stock
            twosigma = sigma * 2
            threesigma = sigma * 3
            price = price_initial
            eps = eps_initial
            quantity = round(PORTFOLIO / price)
            print("")
            print(f"quantity: {quantity} value: {round(price * quantity)}")
            # simulate RANGE years of prices, either annually or in monthly blocks
            for x in range(RANGE):
                probability = roll()
                eps = eps * EPS_GROWTH_RATE
                pe_correction = False
                pe = price / eps
                if (pe / pe_initial) > PE_FACTOR:
                    pe_correction = True

                if probability == 7:
                    price = price * (mu+1)
                # one sigma
                elif probability > 4 and probability < 7:
                    price = price * (mu-sigma+1)
                elif probability > 7 and probability < 10:
                    if pe_correction:
                        price = price * (mu-sigma+1)
                    else:
                        price = price * (mu+sigma+1)
                # two sigma
                elif probability > 2 and probability < 5:
                    price = price * (mu-twosigma+1)
                elif probability > 9 and probability < 12:
                    if pe_correction:
                        price = price * (mu-twosigma+1)
                    else:
                        price = price * (mu+twosigma+1)
                # three sigma
                elif probability == 2:
                    price = price * (mu-threesigma+1)
                elif probability == 12:
                    if pe_correction:
                        price = price * (mu-threesigma+1)
                    else:
                        price = price * (mu+threesigma+1)
                        
            
                # cant have negative prices
                if price < 0 or price < 0.0:
                    price = 0
                    print(f"{price}")
                    if x == RANGE-1:
                        value = round(price * quantity)
                        if value == 0:
                            zero_count = zero_count + 1
                            zero_stocks.append(stockticker)
                        final_value = final_value + value
                        print(f"quantity: {quantity} value: {value}")
                    continue
                simulated_pe = round(price / eps, 2)
                print(f"{round(price, 2)}   {simulated_pe}")
                if x == RANGE-1:
                    value = round(price * quantity)
                    if value == 0:
                        zero_count = zero_count + 1
                        zero_stocks.append(stockticker)
                    final_value = final_value + value
                    print(f"quantity: {quantity} value: {value}")
            # time.sleep(1)
        final_values.append(final_value)
        print("")
        print(f"portfolio: {final_value}")
    print("")
    for item in final_values:
        print(f" : {item}")
    for stock in stocks:
        print(f"{stock[0]}          {stock[1]}  {stock[2]}  {stock[3]}")
    # for stock in zero_stocks:
    #     print(f"{stock}")
    print("")
    print(f"zero_count: {zero_count}")


def main(args):
    stocks = args
    stocks.pop(0)
    simulate(get_stats(stocks))


if __name__ == "__main__":
    main(sys.argv)
