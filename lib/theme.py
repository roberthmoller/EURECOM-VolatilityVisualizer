import streamlit as st


class Theme:
    pc = st.get_option('theme.primaryColor')
    bc = st.get_option('theme.backgroundColor')
    sbc = st.get_option('theme.secondaryBackgroundColor')
    tc = st.get_option('theme.textColor')
