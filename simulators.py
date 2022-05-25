import enum
from typing import Any
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
from pulp import LpMinimize, LpProblem, LpVariable, LpStatus


def zero_bond(par = 100, discount_rate = 0.13, maturity = 5):
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
    ax.set_xticks(lenght)
    ax.set_xticklabels(lenght)
        
    return PV, fig

def coupon_bond(par = 100, coupon_rate = 0.2, discount_rate = 0.13, maturity = 5, yearly = True) -> Any:
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

def stock(tick:str) -> pd.DataFrame:
    data = yf.Ticker(tick) # Generel ticker info
    ticker_data = data.history(period="5y", interval="1mo", rounding=True) # obtaining 5 year data for any requested ticker
    ticker_data.dropna(inplace = True) #deleting random empty spots
    ticker_data = pd.DataFrame(ticker_data["Close"])
    ticker_data.rename(columns = {"Close": tick}, inplace=True)
    return ticker_data

class portfolio():
    def __init__(self, tickers, name = "Default_Portfolio") -> None:
        self.name = name
        self.tickers = tickers
        self.origin_portfolio = None
        self.origin_weights = {}
        self.weighted_portfolio = None
        self.new_weights = {}

    def repr(self) -> pd.DataFrame:
        # return visual representation of the current portfolio
        return self.origin_portfolio

    def create_portfolio(self):
        # Portfolio generation method. Weights will be created automatically for consistency
        for i, ticker in enumerate(self.tickers):
            if i == 0:
                self.origin_portfolio = ticker
            else:
                self.origin_portfolio = pd.concat([self.origin_portfolio, ticker], axis=1)
        
        equal_weight = 1/len(self.tickers)
        for ticker in self.origin_portfolio.columns:
            self.origin_weights[ticker] = equal_weight

    def origin_stocks_returns(self):
        # Display the average monthly return for each stock for the period
        return self.origin_portfolio.pct_change().mean(axis=0)

    def origin_volatility(self):
        # Display the average monthly return for each stock for the period
        return self.origin_portfolio.pct_change().std(axis=0)

    def portfolio_return(self):
        # calculate expected portfolio return for the baseline case of equal weights
        pass