import dataclasses

import graphviz as graphviz
import pandas as pd
import streamlit as st

# Set server.maxUploadSize to suitable size for vmem file
from lib.timeline import Timeline, Slide, DateTime, Text

st.set_page_config(
    page_title="Analysis - Volatility Visualizer",
    page_icon="🔬",
    layout="wide",
)


class Component:
    def render(self):
        raise NotImplementedError('render() must be implemented by subclass')

    def __post_init__(self):
        self.render()


with st.sidebar:
    files = st.file_uploader("", accept_multiple_files=True)
    st.info("Please upload files to visualize")

    if files:
        file_dict = {}
        for file in files:
            file_dict[file.name] = {'file': file}

st.title("Analysis")

if len(files) == 0:
    st.warning("No files to analyze")
    st.stop()

# st.header("Summary")
# st.metric("Files", len(analyze_files))


# metrics of files
# timeline of events


# For each file in files
# st.header("Analysis 1")
import csv
from re import sub
from dataclasses import dataclass


class Theme:
    pc = st.get_option('theme.primaryColor')
    bc = st.get_option('theme.backgroundColor')
    sbc = st.get_option('theme.secondaryBackgroundColor')
    tc = st.get_option('theme.textColor')


class PSTree:
    class PS:
        def __init__(self, row):
            self.name = str(row[1])
            self.pid = int(row[2])
            self.ppid = int(row[3])
            self.threads = int(row[4])
            self.hnds = int(row[5])
            date = str(row[6]).split('-')
            time = str(row[7]).split(':')
            self.date = DateTime(date[0], date[1], date[2], time[0], time[1], time[2])
            self.timezone = row[8]

        def __repr__(self):
            return f"PS(name: {self.name}, pid: {self.pid}, ppid: {self.ppid}, threads: {self.threads}, hnds: {self.hnds}, date: {self.date}, timezone: {self.timezone})"

    def __init__(self, file):
        self.content = file.read().decode('utf-8')
        stripped = sub(" +", ',', self.content)
        lines = stripped.splitlines()
        header = lines[0].upper().split(',')
        header.insert(0, 'LEVEL')
        header.append('ZONE')

        data = [row.split(',') for row in lines[2:]]  # skip [1] as it is a horizontal line # todo make private
        for index, row in enumerate(data):
            data[index][0] = len(row[0])
            data[index][-3] = ' '.join(row[-3:-1])
            del data[index][-2]

        self.df = pd.DataFrame(data=data, columns=header)

    def __str__(self):
        return self.content

    def graph(self):

        digraph = graphviz.Digraph(
            node_attr={'shape': 'record', 'fontsize': '8', 'height': '0.3', 'width': '1.5'},
            graph_attr={'splines': 'ortho', 'bgcolor': Theme.bc},
        )
        self.df.sort_values(by=['TIME'])
        time_groups = self.df.groupby('TIME').groups
        digraph.attr(compound='true')

        for index, (time, group) in enumerate(time_groups.items()):
            with digraph.subgraph(name=f't{index}') as c:
                c.attr(rank='same', style='filled', fillcolor='red')
                two_line_time = time.replace(' ', '\n')
                c.node(f'time{index}', f"{two_line_time}", shape='plaintext', fontcolor=Theme.tc)
                for row_index in group:
                    row = self.df.iloc[row_index]
                    c.node(row['PID'], f"""
                    {{NAME|PID|THDS|HNDS}}|
                    {{{row['NAME']}|{row['PID']}|{row['THDS']}|{row['HNDS']}}}
                    """, fillcolor=Theme.sbc, style='filled', fontcolor=Theme.tc)
            if index != 0:
                digraph.edge(f'time{index - 1}', f'time{index}', style='invis')

        for index, row in self.df.iterrows():
            if row['LEVEL'] != 0:
                digraph.edge(row['PPID'], row['PID'], arrowhead='vee', color=Theme.tc)

        return digraph


for file in files:
    with st.expander(file.name):
        col = st.columns(4)
        col[0].metric('Name', file.name)
        col[1].metric('Type', file.type, 'mime')
        col[2].metric('Size', file.size, 'bytes')
        col[3].selectbox('Extract', ['strings', 'procdump', 'pstree'], key=file.name)

        st.subheader("Content")
        pstree = PSTree(file)
        st.code(pstree.content)
        st.graphviz_chart(pstree.graph())