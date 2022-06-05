import attrs
import streamlit as st

# Set server.maxUploadSize to suitable size for vmem file
from timeline import Slide, Text, DateTime, Timeline

st.set_page_config(
    page_title="Volatility Visualizer",
    page_icon="🔥",
    layout="wide",
)

st.title("Volatility Visualizer")
st.text("This is a simple tool to visualize volatility data.")

with st.sidebar:
    st.header("Select a file")
    files = st.file_uploader("Upload a volatility files", accept_multiple_files=True)

if len(files) > 0:
    st.write("You uploaded:", files)
else:
    st.info("Please upload a memfile")

st.header("Summary")

Timeline(
    height=300,
    events=[
        Slide(
            group="group1",
            start_date=DateTime(year='2020'),
            text=Text(
                headline="Volatility Visualizer",
                text='foo'
            )
        ),
        Slide(
            group="group2",
            start_date=DateTime(year='2020'),
            text=Text(
                headline="Volatility Visualizer",
                text='foo'
            )
        ),
        Slide(
            group="group3",
            start_date=DateTime(year='2020'),
            text=Text(
                headline="Volatility Visualizer",
                text='foo'
            )
        ),
    ],
)

# metrics of files
# timeline of events


# For each file in files
# st.header("Analysis 1")
