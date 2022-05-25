# THIS IS THE MAIN FILE

import streamlit as st
import simulators

value, plot = simulators.coupon_bond(maturity=10, discount_rate=0.05)
st.pyplot(plot)


stock1= simulators.stock("MSFT")
stock2= simulators.stock("AAPL")
stock3= simulators.stock("WM")
stocks = [stock1, stock2, stock3]

portfolio = simulators.portfolio(stocks)

portfolio.create_portfolio()

st.write(portfolio.repr())
