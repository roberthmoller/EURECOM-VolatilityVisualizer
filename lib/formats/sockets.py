from re import sub

import numpy as np
import streamlit as st
from pandas import DataFrame

from lib.file import File
from lib.formats.extract import Extract, section


class Sockets(Extract):
    def __init__(self, file: File) -> None:
        """We parse the file into a dataframe for this format"""
        super().__init__(file)
        lines = sub(" +", ',', self.data).splitlines()
        header = lines[0].upper().split(',')[:-2]
        data = [row.split(',')[:-3] for row in lines[2:]]

        self.df = DataFrame(data=data, columns=header) \
            .drop(['OFFSET(V)'], axis=1) \
            .set_index('PID')

    def content(self) -> None:
        pass

    @section('Dynamic Selection')
    def table(self):
        c = st.columns((1, 1, 1, 2, 2))
        filters = ['', '', '', '', '']
        filters[0] = 'PID == "' + c[0].selectbox('PID', ['Any'] + list(set(map(str, self.df.index)))) + '"'
        filters[1] = 'PORT == "' + c[1].selectbox('PORT', ['Any'] + list(set(map(str, self.df['PORT'])))) + '"'
        filters[2] = 'PROTO == "' + c[2].selectbox('PROTO', ['Any'] + list(set(map(str, self.df['PROTO'])))) + '"'
        filters[3] = 'PROTOCOL == "' + c[3].selectbox('PROTOCOL', ['Any'] + list(set(map(str, self.df['PROTOCOL'])))) + '"'
        filters[4] = 'ADDRESS == "' + c[4].selectbox('ADDRESS', ['Any'] + list(set(map(str, self.df['ADDRESS'])))) + '"'
        filters = [fil for fil in filters if not fil.endswith('Any"')]
        if len(filters) > 0:
            st.table(self.df.query(' & '.join(filters)))
        else:
            st.table(self.df)
