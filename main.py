# THIS IS THE MAIN FILE

import streamlit as st
import simulators

value, plot = simulators.coupon_bond()
st.pyplot(plot)


# simulators.portfolio()