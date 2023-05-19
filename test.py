import streamlit as st
import numpy as np
import pandas as pd

import streamlit as st
import pandas as pd


st.write('Hello, *World!* :sunglasses:')

code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language='python')

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)


x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)