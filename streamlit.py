import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime


export = pd.read_csv(f'exports/export_{datetime.now().strftime("%Y-%m-%d")}.csv')
keywords = pd.read_csv(f'exports/keywords_{datetime.now().strftime("%Y-%m-%d")}.csv')


st.write("The data I am working with:")
st.write(export)

st.write("List of most frequently recurring keywords:")
st.write(keywords)

st.write("A simple line chart:")
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)