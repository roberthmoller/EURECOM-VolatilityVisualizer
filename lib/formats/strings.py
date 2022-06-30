from pandas import DataFrame

from lib.file import File
from lib.formats.extract import Extract, section
import streamlit as st
from re import findall
class Strings(Extract):
    # email = r"/^(([^<>()[\]\\.,;:\s@]+(\.[^<>()[\]\\.,;:\s@]+)*)|(.+))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/"
    # phone = r"(\+420)?(\s*)?(\d{3})(\s*)?\(d{3})(\s*)?\(d{3})"
    word = r"[a-zA-Z0-9\\]{30,}"
    regex = f"({word})"

    def __init__(self, file: File) -> None:
        super().__init__(file)

    def content(self) -> None:
        pass

    @section("Words longer than 30chr's")
    def table(self):
        matches = findall(self.regex, self.data)
        self.df = DataFrame(matches)
        st.dataframe(self.df)