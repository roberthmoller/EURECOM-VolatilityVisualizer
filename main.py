import attrs
import streamlit as st
from streamlit_timeline import timeline

# Set server.maxUploadSize to suitable size for vmem file

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
timeline({
    'events': [
        {
            'start_date': {'year': '2022', 'month': '01', 'day': '01', 'hour': '12', 'minute': '00'},
            'title': 'event 1',
            'group': 'Processes',
            'text': {
                'headline': 'event 2',
                'text': 'This is a test event',
            },
        },
        {
            'start_date': {'year': '2022', 'month': '01', 'day': '01', 'hour': '12', 'minute': '00'},
            'text': {
                'headline': 'event 2',
                'text': 'This is a test event',
            },
            'group': 'Connections',
        },
    ],
}, height=500)
# metrics of files
# timeline of events


# For each file in files
# st.header("Analysis 1")
