from abc import ABC

import streamlit as st

from lib.file import File


def section(title: str, expanded: False = False):
    def decorate(fn):
        def wrapper(*args, **kwargs):
            with st.expander(title, expanded=expanded):
                return fn(*args, **kwargs)

        wrapper.is_section = True
        return wrapper

    return decorate


class ExtractCore:
    def __init__(self):
        self.sections = [getattr(self, field) for field in dir(self) if hasattr(getattr(self, field), 'is_section')]

    def render(self) -> None:
        [render() for render in self.sections]

    @section("Content")
    def content(self) -> None:
        st.code(self.data)


class Extract(ABC, ExtractCore):
    types = {}

    def __init__(self, file: File) -> None:
        super().__init__()
        self.file = file
        self.data = file.read().decode('utf-8')

    def __init_subclass__(cls, key: str = None, priority: int = 1, **kwargs) -> None:
        super().__init_subclass__()
        cls.key = cls.__name__.lower() if key is None else key
        cls.priority = priority
        cls.types[cls.key] = cls

    def __class_getitem__(cls, item):
        return cls.types[item]

    def __str__(self):
        return self.content
