import sys
import random
import time
import yfinance as yf
import statistics
from crawler import convert_currency


UNIVERSES = 100
RANGE = 20
PORTFOLIO = 10000


def roll():
    first = random.randint(1,6)
    second = random.randint(1,6)
    probability = first + second
    return probability


def get_prices(stocks):
    tickers = yf.Tickers(stocks)
    prices = []
    for stock in tickers.tickers:
        info = tickers.tickers[stock].info
        keys = info.keys()
        currency = info["currency"] if "currency" in keys else 0
        price = round(convert_currency(info["currentPrice"], currency), 2) if "currentPrice" in keys else 0
        prices.append(price)
    return prices


def get_stats(stocks):
    data = yf.download(stocks, period="5y", interval="3mo")
    individual_prices = data["Adj Close"]
    mus = []
    sigmas = []
    for stock in stocks:
        if len(stocks) == 1:
            prices = individual_prices.pct_change().tolist()
        else:
            prices = individual_prices[stock].pct_change().tolist()
        prices = [x for x in prices if str(x) != 'nan']
        n = len(prices)
        total = sum(prices)
        mu = round(total/n, 2)
        sigma = round(statistics.stdev(prices), 2)
        mus.append(mu)
        sigmas.append(sigma)
    prices = get_prices(stocks)
    return list(zip(prices, mus, sigmas))


def simulate(stocks):   
    zero_count = 0
    # mulitple universes
    final_values = []
    for x in range(UNIVERSES):
        final_value = 0
        for stock in stocks:
            (price_initial, mu, sigma) = stock
            twosigma = sigma * 2
            threesigma = sigma * 3
            price = price_initial
            quantity = round(PORTFOLIO / price)
            print("")
            print(f"quantity: {quantity} value: {round(price * quantity)}")
            # simulate 10 years of prices
            for x in range(RANGE):
                probability = roll()
                if probability == 7:
                    price = price * (mu+1)
                # one sigma
                elif probability > 4 and probability < 7:
                    price = price * (mu-sigma+1)
                elif probability > 7 and probability < 10:
                    price = price * (mu+sigma+1)
                # two sigma
                elif probability > 2 and probability < 5:
                    price = price * (mu-twosigma+1)
                elif probability > 9 and probability < 12:
                    price = price * (mu+twosigma+1)
                # three sigma
                elif probability == 2:
                    price = price * (mu-threesigma+1)
                elif probability == 12:
                    price = price * (mu+threesigma+1)
                
                # cant have negative prices
                if price < 0 or price < 0.0:
                    price = 0
                    print(f"{price}")
                    if x == RANGE-1:
                        value = round(price * quantity)
                        if value == 0:
                            zero_count = zero_count + 1
                        final_value = final_value + value
                        print(f"quantity: {quantity} value: {value}")
                    continue
                print(f"{round(price, 2)}")
                if x == RANGE-1:
                    value = round(price * quantity)
                    if value == 0:
                        zero_count = zero_count + 1
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
        print(f"{stock[0]}      {stock[1]}  {stock[2]}")
    print("")
    print(f"zero_count: {zero_count}")


def main(args):
    stocks = args
    stocks.pop(0)
    simulate(get_stats(stocks))


if __name__ == "__main__":
    main(sys.argv)
