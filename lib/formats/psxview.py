from re import sub

import pandas as pd
import streamlit as st

from lib.file import File
from lib.formats.extract import Extract, section
from lib.mapcoloumn import mapColumn


class PSXView(Extract):
    def __init__(self, file: File) -> None:
        """We parse the file into a dataframe for this format"""
        super().__init__(file)
        lines = sub(" +", ',', self.data).splitlines()
        header = lines[0].upper().split(',')
        data = [row.split(',') for row in lines[2:]]

        check = '✅'
        cross = ' '
        self.df = pd.DataFrame(data=data, columns=header) \
            .drop(['OFFSET(P)', 'EXITTIME'], axis=1).set_index('PID') \
            .pipe(mapColumn('PSLIST', lambda pslist: check if pslist == 'True' else cross)) \
            .pipe(mapColumn('PSSCAN', lambda psscan: check if psscan == 'True' else cross)) \
            .pipe(mapColumn('THRDPROC', lambda thrdproc: check if thrdproc == 'True' else cross)) \
            .pipe(mapColumn('PSPCID', lambda pspcid: check if pspcid == 'True' else cross)) \
            .pipe(mapColumn('CSRSS', lambda csrss: check if csrss == 'True' else cross)) \
            .pipe(mapColumn('SESSION', lambda session: check if session == 'True' else cross)) \
            .pipe(mapColumn('DESKTHRD', lambda deskthrd: check if deskthrd == 'True' else cross))

        print(self.df)

    def content(self) -> None:
        pass

    @section('Cross Reference Table')
    def table(self):
        st.table(self.df)
