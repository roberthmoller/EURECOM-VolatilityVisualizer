from lib.formats.extract import Extract
from re import sub
from lib.file import File
from re import sub

import graphviz as graphviz
import pandas as pd
import streamlit as st

from lib.file import File
from lib.mapcoloumn import mapColumn
from lib.theme import Theme
from lib.formats.extract import Extract, section




class ConnScan(Extract):
    class Columns:
        offset = 0
        local_address = 1
        local_port = 2
        remote_address = 3
        remote_port = 4
        pid = 5

    def __init__(self, file: File) -> None:
        """We parse the file into a dataframe for this format"""
        super().__init__(file)
        lines = self.data.splitlines()
        header = sub(" {2,}", ',', lines[0]).upper().split(',')
        data = [sub(" +", ',', row).split(',') for row in lines[2:]]

        self.df = pd.DataFrame(data=data, columns=header)

        self.df = self.df \
            .assign(LPort=self.df['LOCAL ADDRESS'].map(lambda addr: addr.split(":")[-1])) \
            .assign(RPort=self.df['REMOTE ADDRESS'].map(lambda addr: addr.split(":")[-1])) \
            .rename(columns={'RPort': 'REMOTE PORT', 'LPort': 'LOCAL PORT'}) \
            .reindex(columns=['OFFSET(P)', 'LOCAL ADDRESS', 'LOCAL PORT', 'REMOTE ADDRESS', 'REMOTE PORT', 'PID']) \
            .pipe(mapColumn('LOCAL ADDRESS', lambda addr: addr.split(':')[0])) \
            .pipe(mapColumn('REMOTE ADDRESS', lambda addr: addr.split(':')[0]))

        print(self.df)

    def content(self) -> None:
        pass

    @section("Visualization")
    def visualize(self):
        """We visualize a timeline graph of the processes over time and their relationship"""
        g = graphviz.Digraph(
            node_attr={'shape': 'record', 'fontsize': '8', 'height': '0.3', 'width': '1.5'},
            graph_attr={'splines': 'ortho', 'bgcolor': Theme.bc},
        )

        laddr_groups = self.df.groupby('PID').groups
        g.attr(compound='true')

        for index, (PID, group) in enumerate(laddr_groups.items()):
            with g.subgraph(name=f'host#{PID}') as c:
                c.attr(style='filled', fillcolor='red')
                c.node(f'pid#{PID}', f"PROCESS| {{PID|{PID}}}", fillcolor=Theme.sbc, style='filled', fontcolor=Theme.tc)

                for row_index in group:
                    row = self.df.iloc[row_index]

                    g.edge(f"pid#{PID}", f"port#{row['LOCAL PORT']}", color='white', fontcolor=Theme.tc)
                    # c.node(f"port#{row['LOCAL PORT']}", f"LOCAL| {{PORT|{row['LOCAL PORT']}}}", fillcolor=Theme.sbc, style='filled', fontcolor=Theme.tc)
                    c.node(f"port#{row['LOCAL PORT']}", f"LOCAL| {{ADDRESS|{row['LOCAL ADDRESS']}}}|{{PORT|{row['LOCAL PORT']}}}", fillcolor=Theme.sbc, style='filled', fontcolor=Theme.tc)

                    g.edge(f"port#{row['LOCAL PORT']}", f"host#{row['REMOTE ADDRESS']}", color='white', fontcolor=Theme.tc)
                    c.node(f"host#{row['REMOTE ADDRESS']}", f"REMOTE| {{ADDRESS|{row['REMOTE ADDRESS']}}}|{{PORT|{row['REMOTE PORT']}}}", fillcolor=Theme.sbc, style='filled', fontcolor=Theme.tc)

        st.graphviz_chart(g)

# EXamples
#
# graph with box for each ip address and lines for each port
# class Columns:
#     level: int = 0
#     name: int = 1
#     pid: int = 2
#     ppid: int = 3
#     threads: int = 4
#     hnds: int = 5
#     date: int = 6
#     time: int = 7
#     timezone: int = 8

# def __init__(self, file: File) -> None:
#     """We parse the file into a dataframe for this format"""
#     super().__init__(file)
#     stripped = sub(" +", ',', self.data)
#     lines = stripped.splitlines()
#     header = lines[0].upper().split(',')
#     header.insert(0, 'LEVEL')
#     header.append('ZONE')

#     data = [row.split(',') for row in lines[2:]]  # skip [1] as it is a horizontal line
#     for index, row in enumerate(data):
#         data[index][self.Columns.level] = len(row[self.Columns.level])
#         data[index][self.Columns.date] = ' '.join(row[self.Columns.date:self.Columns.timezone])
#         del data[index][-2]

#     self.df = pd.DataFrame(data=data, columns=header)

# @section("Visualization")
# def visualize(self):
#     """We visualize a timeline graph of the processes over time and their relationship"""
#     g = graphviz.Digraph(
#         node_attr={'shape': 'record', 'fontsize': '8', 'height': '0.3', 'width': '1.5'},
#         graph_attr={'splines': 'ortho', 'bgcolor': Theme.bc},
#     )
#     self.df.sort_values(by=['TIME'])
#     time_groups = self.df.groupby('TIME').groups
#     g.attr(compound='true')

#     for index, (time, group) in enumerate(time_groups.items()):
#         with g.subgraph(name=f't{index}') as c:
#             c.attr(rank='same', style='filled', fillcolor='red')
#             two_line_time = time.replace(' ', '\n')
#             c.node(f'time{index}', f"{two_line_time}", shape='plaintext', fontcolor=Theme.tc)
#             for row_index in group:
#                 row = self.df.iloc[row_index]
#                 c.node(row['PID'], f"""
#                 {{NAME|PID|THDS|HNDS}}|
#                 {{{row['NAME']}|{row['PID']}|{row['THDS']}|{row['HNDS']}}}
#                 """, fillcolor=Theme.sbc, style='filled', fontcolor=Theme.tc)
#         if index != 0:
#             g.edge(f'time{index - 1}', f'time{index}', style='invis')

#     for index, row in self.df.iterrows():
#         if row['LEVEL'] != 0:
#             g.edge(row['PPID'], row['PID'], arrowhead='vee', color=Theme.tc)

#     st.graphviz_chart(g)
