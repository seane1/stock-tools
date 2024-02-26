import sys
import time
import random
from utils import *


UNIVERSES = 100
RANGE = 10
PORTFOLIO = 10000
PE_FACTOR = 2.5
EPS_GROWTH_RATE = 1.1


def roll():
    first = random.randint(1,6)
    second = random.randint(1,6)
    probability = first + second
    return probability


def simulate(stocks):
    zero_stocks = []
    zero_count = 0
    final_values = []
    # mulitple universes
    for x in range(UNIVERSES):
        final_value = 0
        for stock in stocks:
            (stockticker, price_initial, mu, sigma, eps_initial, pe_initial, beta) = stock
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
            time.sleep(1)
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
    if len(args) == 0:
        print("running in filter mode")
        stocks = get_stocks("asx.csv")
        # stocks.extend(get_stocks("sp500.csv"))
        # stocks.extend(get_stocks("nikkei.csv"))
    simulate(get_stats(stocks))


if __name__ == "__main__":
    main(sys.argv)
