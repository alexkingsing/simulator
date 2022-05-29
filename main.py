# THIS IS THE MAIN FILE

from matplotlib import ticker
import streamlit as st
import simulators

st.set_page_config(layout="wide")

st.title(body = "Capital Budgeting sandbox app", anchor="Title")

with st.sidebar:
    option = st.selectbox("Choose what you want to evaluate", ["","Bonds", "Stocks & Portfolio", "Project NPV"], 0)

if option == "":
    st.write("Cool")

elif option == "Bonds":  ### PENDING DESCRIPTION FOR BOTH BOND TYPES
    col1, col2 = st.columns([2,1])

    with col1: # bonds description
        pass

    with col2: # bonds choice
        choice = st.radio("Choose the type of bond to review", ["Zero", "Coupon"])

    if choice == "Zero":
        st.write("SOME INTRO TEXT TO A ZERO BOND")
        zcol1, zcol2, zcol3 = st.columns(3)
        with zcol1:
            face_value = st.number_input("Input the face value/par of the bond", min_value=0, value=100)
        with zcol2:
            rate = st.number_input("Input the discount rate for the bond (0 to 1)", min_value=0.0, max_value=1.0, step=0.01, value=0.1)
        with zcol3:
            time_to_maturity = st.number_input("Input the maturity of the bond (years from now", min_value=1, value=5)

        display = st.button("Plot and value!")
        if display == True:
            value, plot = simulators.zero_bond(par=face_value, discount_rate=rate, maturity = time_to_maturity)
            st.pyplot(plot)

    else:
        st.write("SOME INTRO TEXT TO A COUPON BOND")
        ccol1, ccol2, ccol3, ccol4, ccol5 = st.columns(5)
        with ccol1:
            face_value = st.number_input("Input the face value/par of the bond", min_value=0, value=100)
        with ccol2:
            rate = st.number_input("Input the discount rate for the bond (0 to 1)", min_value=0.0, max_value=1.0, step=0.01, value=0.1)
        with ccol3:
            time_to_maturity = st.number_input("Input the maturity of the bond (years from now", min_value=1, value=5)
        with ccol4:
            coupon = st.number_input("Input the coupon rate for the bond (0 to 1)", min_value=0.0, max_value=1.0, step=0.01, value=0.1)
        with ccol5:
            frequency = st.checkbox("Yearly payments frequency?", value=True)


        display = st.button("Plot and value!")
        if display == True:
            value, plot = simulators.coupon_bond(par=face_value, discount_rate=rate, 
            maturity=time_to_maturity, coupon_rate=coupon, yearly=frequency)
            st.pyplot(plot)

elif option == "Stocks & Portfolio":

    tickers = st.text_area("Input the tickers you'd like to review (max 10) separated by coma", value="")
    tickers = tickers.replace(" ","")
    st.caption("Tickers that cannot be retrieved will be omitted to not interrupt runtime. A warning will be displayed."    )
    tickers_list = tickers.split(sep=",")

    st.write(tickers, tickers_list)

    # creating stocks list through list comprehension
    stocks_data = [simulators.stock(ticker) for ticker in tickers_list]

    st.write(len(stocks_data))
    st.write(stocks_data[0])

    

    '''
    stock1= simulators.stock("MSFT")
    stock2= simulators.stock("AAPL")
    stock3= simulators.stock("WM")
    stocks = [stock1, stock2, stock3]

    portfolio = simulators.portfolio(stocks)

    portfolio.create_portfolio()

    st.write(portfolio.portfolio_volatility())
    '''

else:
    pass
