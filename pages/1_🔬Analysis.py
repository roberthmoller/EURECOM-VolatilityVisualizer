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
        header.insert(-1, 'DATE')
        header.append('ZONE')
        data = [row.split(',') for row in lines[2:]]  # skip [1] as it is a horizontal line # todo make private
        for index, row in enumerate(data):
            data[index][0] = len(row[0])

        self.df = pd.DataFrame(data=data, columns=header)

    def __str__(self):
        return self.stripped

    def graph(self):
        digraph = graphviz.Digraph(
            node_attr={'shape': 'box', 'fontsize': '14', 'height': '.1', 'width': '1'},
            graph_attr={'size': '10,10'}
        )
        self.df.sort_values(by=['TIME'])

        for index, row in self.df.iterrows():
            with digraph.subgraph() as c:
                c.attr(rank='same')
                c.node(f'time{index}', f'{row["DATE"]}\n{row["TIME"]}', shape='plaintext')
                c.node(row['PID'], row['NAME'])

            if index != 0:
                digraph.edge(f'time{index - 1}', f'time{index}')

        for index, row in self.df.iterrows():
            if row['LEVEL'] != 0:
                digraph.edge(row['PPID'], row['PID'])

        return digraph

        # digraph shells {
        #     size="7,8";
        #     node [fontsize=24, shape = plaintext];
        #
        #     1972 -> 1976;
        #     1976 -> 1978;
        #     1978 -> 1980;
        #     1980 -> 1982;
        #     1982 -> 1984;
        #     1984 -> 1986;
        #     1986 -> 1988;
        #     1988 -> 1990;
        #     1990 -> future;
        #
        #     node [fontsize=20, shape = box];
        #     { rank=same;  1976 Mashey Bourne; }
        #     { rank=same;  1978 Formshell csh; }
        #     { rank=same;  1980 esh vsh; }
        #     { rank=same;  1982 ksh "System-V"; }
        #     { rank=same;  1984 v9sh tcsh; }
        #     { rank=same;  1986 "ksh-i"; }
        #     { rank=same;  1988 KornShell Perl rc; }
        #     { rank=same;  1990 tcl Bash; }
        #     { rank=same;  "future" POSIX "ksh-POSIX"; }
        #
        #     Thompson -> Mashey;
        #     Thompson -> Bourne;
        #     Thompson -> csh;
        #     csh -> tcsh;
        #     Bourne -> ksh;
        #     Bourne -> esh;
        #     Bourne -> vsh;
        #     Bourne -> "System-V";
        #     Bourne -> v9sh;
        #     v9sh -> rc;
        #     Bourne -> Bash;
        #     "ksh-i" -> Bash;
        #     KornShell -> Bash;
        #     esh -> ksh;
        #     vsh -> ksh;
        #     Formshell -> ksh;
        #     csh -> ksh;
        #     KornShell -> POSIX;
        #     "System-V" -> POSIX;
        #     ksh -> "ksh-i";
        #     "ksh-i" -> KornShell;
        #     KornShell -> "ksh-POSIX";
        #     Bourne -> Formshell;
        #
        #     edge [style=invis];
        #     1984 -> v9sh -> tcsh ;
        #     1988 -> rc -> KornShell;
        #     Formshell -> csh;
        #     KornShell -> Perl;
        # }


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
        # st.dataframe(pstree.df)
        st.graphviz_chart(pstree.graph())
        # st.json(pstree.data)
        # st.json(pstree.tree)
        # st.graphviz_chart("""
        #     digraph G {
        #       edge [arrowhead=none];
        #       nodesep = 0.1;
        #       ranksep=0.5;
        #       splines = ortho;
        #       rankdir = LR;
        #
        #       node [ shape="box" ];
        #       A1 B4 B5 B6 B3 B2 B1;
        #
        #       node [ shape="point", width = 0, height = 0 ];
        #       { rank = same; W4 W5 W6 W0 W3 W2 W1 }
        #
        #       A1 -> W0;
        #       W4 -> W5 -> W6 -> W0 -> W3 -> W2 -> W1;        /* critical! */
        #       W1 -> B1;
        #       W2 -> B2;
        #       W3 -> B3;
        #       W4 -> B4;
        #       W5 -> B5;
        #       W6 -> B6;
        #     }
        # """)
        # Timeline(
        #     height=400,
        #     events=[
        #         Slide(
        #             start_date=ps.date,
        #             text=Text(
        #                 headline=ps.name,
        #                 text=f"pid: {ps.pid}\nppid: {ps.ppid}\nthreads: {ps.threads}\nhnds: {ps.hnds}\n{ps.date}",
        #             ),
        #
        #         )
        #         for ps in pstree.tree.values()]
        # )

    #
    # def render(self):
    #     st.subheader("PSTree")
    #     st.code(self.processes)
