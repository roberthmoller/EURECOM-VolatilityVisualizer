import streamlit as st

st.set_page_config(
    page_title="Volatility Visualizer",
    page_icon="🏠",
)

readme = open('README.md', 'r').read()
st.markdown(readme)

with st.sidebar:
    st.subheader("Links")
    st.markdown("[github/volatility-visualizer](https://github.com/roberthmoller/volatility-visualizer)")
