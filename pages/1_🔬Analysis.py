import os
import sys

from typing import List

import streamlit as st
from streamlit.uploaded_file_manager import UploadedFile, UploadedFileRec

from lib.formats import *

from lib.formats.extract import Extract
from lib.guessers.guesser import TypeGuess

st.set_page_config(
    page_title="Analysis - Volatility Visualizer",
    page_icon="🔬",
    layout="wide",
)

with st.sidebar:
    uploaded = st.file_uploader("Files to analyse", accept_multiple_files=True)
    samples: List[UploadedFile] = list(uploaded)

if len(uploaded) == 0:
    st.warning("Please upload files to start")
    example_path = 'assets/samples'
    examples = os.listdir(example_path)
    selected_examples = st.multiselect("Examples", examples)
    if len(selected_examples) > 0:
        for example_name in selected_examples:
            with open(f'{example_path}/{example_name}', 'rb') as file:
                samples.append(UploadedFile(UploadedFileRec(0, example_name, 'plain/text', file.read())))
elif len(uploaded) > 0:
    st.info("Please select samples to analyse")
    samples = st.multiselect("Samples", uploaded, format_func=lambda sample: sample.name)
elif len(samples) == 0:
    st.stop()

st.title("Analysis")
for sample in samples:
    st.markdown("""---""")
    st.caption(sample.name)
    # with st.expander(sample.name, expanded=True):
    col = st.columns(4)
    col[0].metric('Name', sample.name)
    col[1].metric('Type (mime)', sample.type)
    col[2].metric('Size (bytes)', sample.size)

    sample_type_guess = TypeGuess.of(sample)
    types = list(Extract.types.items())
    sample_type = col[3].selectbox('Extract',
                                   range(0, len(Extract.types)),
                                   key=sample.name,
                                   format_func=lambda i: types[i][0],
                                   index=sample_type_guess)

    # sample_analyser: Type[Extract] = val(sample_type, Extract)

    analysis = types[sample_type][1](sample)
    analysis.render()
    # analyser: Extract = sample_analyser(sample)
    # pstree = PSTree(sample)
    # st.code(pstree.content)
    # analyser.visualize()

working = False
