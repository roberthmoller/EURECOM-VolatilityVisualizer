from math import floor
from time import sleep

import streamlit as st
from pandas import DataFrame

from lib.file import File
from lib.formats.extract import Extract, section


class CMDLine(Extract):

    def __init__(self, file: File) -> None:
        super().__init__(file)
        self.df = DataFrame(self.data.splitlines())

    @section("Loader")
    def content(self):
        progress = st.progress(0)
        groupings = floor(len(self.df) / 10)
        for i in range(1,11):
            progress.progress(i*10)
            st.code(self.df[groupings * (i - 1):groupings * i])
            sleep(1)
