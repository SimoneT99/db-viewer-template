import streamlit as st
from src.view.Interfaces.IStreamLitPage import IStreamLitPage

class BasePage(IStreamLitPage):

    def __init__(self, sections: dict[str, IStreamLitPage]):
        if sections is None:
            raise ValueError("Sections cannot be None")
        self._sections = sections
        self._current_section_key = list(self._sections.keys())[0]

    def render(self, *args, **kwargs) -> None: 
        self._current_section_key = st.sidebar.selectbox("Sections", self.__get_menu_options())
        self.__get_current_section().render(*args, **kwargs)

    def __get_menu_options(self):
        return list(self._sections.keys())
    
    def __get_current_section(self) -> IStreamLitPage:
        return self._sections[self._current_section_key]