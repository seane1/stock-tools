import sys
import random
import time


def roll():
    first = random.randint(1,6)
    second = random.randint(1,6)
    probability = first + second
    return probability


def main(args):
    mu = float(args[2])
    sigma = float(args[3])
    twosigma = sigma * 2
    threesigma = sigma * 3
    zero_count = 0
    # 100 universes
    for x in range(100):
        price = float(args[1])
        quantity = round(10000 / price)
        print("")
        print(f"quantity: {quantity} value: {round(price * quantity)}")
        # simulate 10 years of prices
        for x in range(10):
            probability = roll()
            if probability == 7:
                price = price * ((mu/100)+1)
            # one sigma
            elif probability > 4 and probability < 7:
                price = price * (((mu-sigma)/100)+1)
            elif probability > 7 and probability < 10:
                price = price * (((mu+sigma)/100)+1)
            # two sigma
            elif probability > 2 and probability < 5:
                price = price * (((mu-twosigma)/100)+1)
            elif probability > 9 and probability < 12:
                price = price * (((mu+twosigma)/100)+1)
            # three sigma
            elif probability == 2:
                price = price * (((mu-threesigma)/100)+1)
            elif probability == 12:
                price = price * (((mu+threesigma)/100)+1)
            
            # cant have negative prices
            if price < 0 or price < 0.0:
                price = 0
                print(f"{price}")
                if x == 9:
                    value = round(price * quantity)
                    if value == 0:
                        zero_count = zero_count + 1
                    print(f"quantity: {quantity} value: {value}")
                continue
            print(f"{round(price, 2)}")
            if x == 9:
                value = round(price * quantity)
                if value == 0:
                    zero_count = zero_count + 1
                print(f"quantity: {quantity} value: {value}")
        # time.sleep(1)
    print("")
    print(f"zero_count: {zero_count}")

if __name__ == "__main__":
    main(sys.argv)
