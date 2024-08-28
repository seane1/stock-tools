import sys
from utils import *
from constants import MARKET_VOL
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import matplotlib.ticker as mticker


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
    print(f"\tmu\tdiv5\tsigma\tsharpe\tbeta\tpe\tratio\tname")
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
        # sharpe = stock[10]
        combined_return = annual_return + div_five
        sharpe = round(combined_return / sigma_individual, 2) if sigma_individual != 0 else 0
        sharpes.append(sharpe)
        means.append(mean)
        betas.append(beta_individual)
        sigmas.append(sigma_individual)
        annual_returns.append(combined_return)
        pes.append(pe)
        ratio = round((combined_return / 100) / beta_individual, 2) if beta_individual != 0 and sigma_individual != 0 else 0
        if len(args) == 0:
            # if ratio > 0.6:
            print(f"{code}\t{'%.2f' % combined_return}\t{div_five}\t{sigma_individual}\t{sharpe}\t{beta_individual}\t{pe}\t{ratio}\t{name}")
        else:
            print(f"{code}\t{'%.2f' % combined_return}\t{div_five}\t{sigma_individual}\t{sharpe}\t{beta_individual}\t{pe}\t{ratio}\t{name}")
    n = len(means)
    total = sum(means)
    mu = round(total / n, 2)
    beta = round(sum(betas) / n, 2)
    sigma = round(beta * MARKET_VOL * 100, 2)
    average_return = round(sum(annual_returns) / n, 2)
    pe = round(sum(pes) / n, 2)
    # sharpe = round((mu / sigma), 2)
    sharpe = round((average_return / sigma), 2)
    kelly = round((average_return / sigma**2)*100, 2)
    leverage1 = round(1 / beta, 2)
    leverage2 = round(0.9 / beta, 2)
    gearing1 = round(leverage1 - 1, 2)
    gearing2 = round(leverage2 - 1, 2)
    leveraged_return1 = round((average_return) + (gearing1 * (average_return - MARGIN_COST)), 2)
    leveraged_return2 = round((average_return) + (gearing2 * (average_return - MARGIN_COST)), 2)
    loan = 20000
    # equity = int(loan / gearing2)
    # ratio = (loan / 0.75) / equity
    # margin_call = round(1 - ratio, 2)
    print()
    print(f"mu:\t{average_return}")
    print(f"sigma:\t{sigma}")
    print(f"sharpe:\t{sharpe}")
    print(f"beta:\t{beta}")
    print(f"L:\t{leverage1}")
    print(f"L*Rp:\t{leveraged_return1}")
    # print(f"kelly:\t{kelly}")
    print(f"gear:\t{gearing1}")
    # print(f"call:\t{margin_call}")
    # print(f"loan:\t{loan}")
    # print(f"equity:\t{equity}")
    # print(f"mean:\t{mu}")
    # print(f"pe:\t{pe}")

    if len(args) != 0:
        plot(leveraged_return1, leverage1, sigma)

def plot(leveraged_return, leverage, sigma):
    # Define the parameters for the bell curves
    mean1, std_dev1 = MARKET_MEAN, MARKET_VOL   # Mean and standard deviation for the first curve
    mean2, std_dev2 = leveraged_return / 100, (sigma * leverage) / 100 # Mean and standard deviation for the second curve
    # mean3, std_dev3 = leveraged_return2 / 100, (sigma * leverage2) / 100 # Mean and standard deviation for the third curve

    # Generate data points for each curve
    x = np.linspace(-1, 1, 1000)
    y1 = stats.norm.pdf(x, mean1, std_dev1)
    y2 = stats.norm.pdf(x, mean2, std_dev2)
    # y3 = stats.norm.pdf(x, mean3, std_dev3)

    # Plot the bell curves
    plt.plot(x, y1, label=f'Mean = {mean1:.2%}, Std Dev = {std_dev1:.2%}', color='blue')
    plt.plot(x, y2, label=f'Mean = {mean2:.2%}, Std Dev = {std_dev2:.2%}', color='red')
    # plt.plot(x, y3, label=f'Mean = {mean3:.2%}, Std Dev = {std_dev3:.2%}', color='green')

    # Add vertical lines at the means
    plt.axvline(mean1, color='blue', linestyle='--', linewidth=2)
    plt.axvline(mean2, color='red', linestyle='--', linewidth=2)
    # plt.axvline(mean3, color='green', linestyle='--', linewidth=2)

    # Display mean values as labels on the axis
    plt.text(mean1, 0, f'{mean1:.2%}', color='blue', fontsize=10, ha='center', va='bottom')
    plt.text(mean2, 0, f'{mean2:.2%}', color='red', fontsize=10, ha='center', va='bottom')
    # plt.text(mean3, 0, f'{mean3:.2%}', color='green', fontsize=10, ha='center', va='bottom')

    # Customize the axes
    plt.axhline(0, color='black', linewidth=2)  # Bold horizontal axis
    plt.axvline(0, color='black', linewidth=2)  # Bold vertical axis

    # Format the x-axis to display percentages
    plt.gca().xaxis.set_major_formatter(mticker.PercentFormatter(1))

    # Add title and labels
    plt.title('Market vs. Portfolio Returns')
    plt.xlabel('Return (%)')
    plt.ylabel('Probability Density')

    # Add a legend
    plt.legend()

    # Show the plot
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main(sys.argv)
