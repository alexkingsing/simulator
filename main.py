# THIS IS THE MAIN FILE

import streamlit as st
import simulators

value, plot = simulators.bonds(zero=False, yearly=False)
st.pyplot(plot)


st.write(simulators.portfolio())