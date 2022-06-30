from re import sub

import graphviz as graphviz
import pandas as pd
import streamlit as st

from lib.file import File
from lib.formats.extract import Extract, section
from lib.theme import Theme


class PSTree(Extract):
    class Columns:
        level: int = 0
        name: int = 1
        pid: int = 2
        ppid: int = 3
        threads: int = 4
        hnds: int = 5
        date: int = 6
        time: int = 7
        timezone: int = 8

    def __init__(self, file: File) -> None:
        """We parse the file into a dataframe for this format"""
        super().__init__(file)
        stripped = sub(" +", ',', self.data)
        lines = stripped.splitlines()
        header = lines[0].upper().split(',')
        header.insert(0, 'LEVEL')
        header.append('ZONE')

        data = [row.split(',') for row in lines[2:]]  # skip [1] as it is a horizontal line
        for index, row in enumerate(data):
            data[index][self.Columns.level] = len(row[self.Columns.level])
            data[index][self.Columns.date] = ' '.join(row[self.Columns.date:self.Columns.timezone])
            del data[index][-2]

        self.df = pd.DataFrame(data=data, columns=header)

    def content(self) -> None:
        pass

    @section("Visualization")
    def visualize(self):
        """We visualize a timeline graph of the processes over time and their relationship"""
        g = graphviz.Digraph(
            node_attr={'shape': 'record', 'fontsize': '8', 'height': '0.3', 'width': '1.5'},
            graph_attr={'splines': 'ortho', 'bgcolor': Theme.bc},
        )
        self.df.sort_values(by=['TIME'])
        time_groups = self.df.groupby('TIME').groups
        g.attr(compound='true')

        for index, (time, group) in enumerate(time_groups.items()):
            with g.subgraph(name=f't{index}') as c:
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
                g.edge(f'time{index - 1}', f'time{index}', style='invis')

        for index, row in self.df.iterrows():
            if row['LEVEL'] != 0:
                g.edge(row['PPID'], row['PID'], arrowhead='vee', color=Theme.tc)

        st.graphviz_chart(g)
