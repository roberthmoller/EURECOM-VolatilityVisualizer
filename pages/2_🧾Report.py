import streamlit as st

from lib.pdf import PDF

st.set_page_config(
    page_title="Report - Volatility Visualizer",
    page_icon="🧾",
    layout="wide",
)

st.title("Report")
PDF('REPORT.pdf')