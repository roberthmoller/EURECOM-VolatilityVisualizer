from pandas import DataFrame
from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler

from lib.formats.extract import Extract
from re import sub

import pandas as pd
import streamlit as st

from lib.file import File
from lib.formats.extract import Extract, section
from lib.mapcoloumn import mapColumn
import altair as alt


# chart
class PSList(Extract):
    def __init__(self, file: File) -> None:
        """We parse the file into a dataframe for this format"""
        super().__init__(file)
        lines = sub(" +", ',', self.data).splitlines()
        header = lines[0].upper().split(',')
        data = [row.split(',')[:-1] for row in lines[2:]]
        # print('header', header)
        # print('data', data)
        self.df = pd.DataFrame(data=data, columns=header, ) \
            .drop(['OFFSET(V)', 'PPID', 'EXIT', 'START', ''], axis=1) \
            .replace('-+', '0', regex=True) \
            .fillna('0')

    @section('Chart')
    def chart(self):
        st.bar_chart(self.df.set_index('NAME').drop('PID', axis=1))
        # for column in df.columns:
        #     st.bar_chart(df[])

    @section('Table')
    def table(self):
        st.table(self.df)

    def content(self) -> None:
        pass
