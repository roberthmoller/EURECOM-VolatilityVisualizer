from base64 import b64encode
from dataclasses import dataclass
import streamlit as st


@dataclass
class PDF:
    path: str
    width: str = '100%'
    height: str = '800px'

    def __post_init__(self):
        with open(self.path, "rb") as f:
            data = b64encode(f.read()).decode('utf-8')
            display = f'<iframe src="data:application/pdf;base64,{data}" width="{self.width}" height="{self.height}" type="application/pdf"/>'
            st.markdown(display, unsafe_allow_html=True)
