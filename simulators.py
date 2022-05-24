from typing import Any
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from pulp import LpMinimize, LpProblem, LpVariable, LpStatus

def bonds(par = 100, coupon_rate = 0.2, discount_rate = 0.13, zero = True, maturity = 5, yearly = True) -> Any:
    if zero == True:
        # Valuation using simple present value
        discount_mult = 1/((1+discount_rate)**maturity)
        PV = par * discount_mult

        # Timeline visualization based on matplotlibs timeline example

        ## creating timeline spacing
        lenght = list(range(0,maturity + 1))
        ## Choosing some nice levels
        levels = np.tile([1] + [0] * (len(lenght)-2) + [2], # creating zero timeline by highlighting start and end
                        int(np.ceil(len(lenght)/6)))[:len(lenght)]

        ## Create figure and plot a stem plot with the date
        fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
        ax.set(title=f'''Zero bond valuation timeline\n Par:{par}, Maturity(Y): {maturity}, Discount rate: {discount_rate*100}%''')

        ax.vlines(lenght, 0, levels, color="tab:red", linestyles="dashed")  # The vertical stems.
        ax.plot(lenght, np.zeros_like(lenght), "-o",
                color="k", markerfacecolor="w")  # Baseline and markers on it.

        ## Annotations 
        names = ["Present value: \n" + f"{round(PV, 2)}"] + [""] * (len(lenght)-2) + ["Face value at maturity: \n" + f"{par}"]

        for n, l, r in zip(lenght, levels, names):
            ax.annotate(r, xy=(n, l),
                        xytext=(0, l*3), textcoords="offset points",
                        horizontalalignment="center",
                        verticalalignment="bottom" if l > 0 else "top")

        ## remove y axis and spines and x_axis title
        ax.yaxis.set_visible(False)
        ax.spines[["left", "top", "right"]].set_visible(False)
        ax.set_xlabel("Years", fontweight = 'bold')
            
        return PV, fig

    else:
        ## Two-part valuation using simple present values

        if yearly == True:          
            periodic_coupon = par * coupon_rate
            effective_rate = discount_rate
            periods = maturity
            # PV of face value
            discount_mult = 1/((1+effective_rate)**periods)
            PV_FV = par * discount_mult
            #PV of coupons
            # Splitting formula in 2 parts for debugging purposes
            left_side = periodic_coupon / effective_rate
            right_side = 1-(1/((1+effective_rate)**periods))
            PV_coupons = left_side * right_side

            compound = "Annual"
            PV = PV_FV + PV_coupons

        else:
            # I'm only considering semi-annual as alternative, for lesser complexity
            periodic_coupon = (par * coupon_rate)/2
            effective_rate = discount_rate / 2
            periods = maturity * 2
            # PV of face value
            discount_mult = 1/((1+effective_rate)**periods)
            PV_FV = par * discount_mult
            #PV of coupons
            # Splitting formula in 2 parts for debugging purposes
            left_side = periodic_coupon / effective_rate
            right_side = 1-(1/((1+effective_rate)**periods))
            PV_coupons = left_side * right_side

            compound = "Semi-Annual"
            PV = PV_FV + PV_coupons

        # Timeline visualization based on matplotlibs timeline example

        ## creating timeline spacing
        lenght = list(range(0,periods + 1))
        ## Choosing some nice levels
        levels = np.tile([2] + [1] * (len(lenght)-2) + [3], # creating timeline
                        int(np.ceil(len(lenght)/6)))[:len(lenght)]

        ## Create figure and plot a stem plot with the date
        fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
        ax.set(title=f'''Coupon bond valuation timeline\n Par:{par}, Maturity(Y): {maturity}, Coupon rate: {coupon_rate*100}%, 
        Discount rate: {discount_rate*100}%, Compounding: {compound}''')

        ax.vlines(lenght, 0, levels, color="tab:red", linestyles="dashed")  # The vertical stems.
        ax.plot(lenght, np.zeros_like(lenght), "-o",
                color="k", markerfacecolor="w")  # Baseline and markers on it.

        ## Annotations 
        names = [f"Present value: \n {round(PV,2)}"] + [f"Coupon: \n{periodic_coupon}"] * (len(lenght)-2) + [f"Face value + coupon: \n {par + periodic_coupon}"]

        for n, l, r in zip(lenght, levels, names):
            ax.annotate(r, xy=(n, l),
                        xytext=(0, l*3), textcoords="offset points",
                        horizontalalignment="center",
                        verticalalignment="bottom" if l > 0 else "top")

        ## remove y axis and spines and x_axis title
        ax.yaxis.set_visible(False)
        ax.spines[["left", "top", "right"]].set_visible(False)
        ax.set_xlabel("Periods", fontweight = 'bold')
        ax.set_xticks(lenght)
        ax.set_xticklabels(lenght)

        return PV, fig

def stock(tick):
    pass

class portfolio():
    pass


def portfolio(ticker_list = ["MSFT", "WM", "AAPL"]):
    data = None

    # Extracting tickers information
    for ticker in ticker_list:
        if data is None:
            ticker_info = yf.Ticker(ticker)
            ticker_data = ticker_info.history(period="5y", interval="1mo", rounding=True)
            ticker_data.dropna(inplace = True) #deleting random empty spots
            data_index = ticker_data.index # saving index for dataframe creation
            data = pd.DataFrame(index = data_index, data = {ticker: ticker_data["Close"]})
        else:
            ticker_info = yf.Ticker(ticker)
            ticker_data = ticker_info.history(period="5y", interval="1mo", rounding=True)
            ticker_data.dropna(inplace = True) #deleting random empty spots
            data = pd.concat([data, ticker_data["Close"]], axis=1)
            data.rename(columns={"Close": ticker}, inplace=True)

    returns = data.pct_change()
    # returns.mean(axis=0) returns per stock
    # returns.std(axis=0) monthly volatility

    



    
