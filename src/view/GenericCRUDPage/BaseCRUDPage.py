from typing import Any, Type, TypeVar, override
from sqlmodel import SQLModel
import streamlit as st

from src.services.CRUDService import CRUDService
from src.view.Interfaces.IStreamLitPage import IStreamLitPage
from src.view.Interfaces.IStreamLitFormStrategy import IStreamLitForm

T = TypeVar("T", bound=SQLModel)

class BaseCRUDPage(IStreamLitPage):

    def __init__(self, 
                 CRUDService: CRUDService[Any], type : Type[Any],
                 form_strategy: IStreamLitForm[Any]):
        if CRUDService is None:
            raise ValueError("CRUDService cannot be None")
        self._CrudService = CRUDService
        if type is None:
            raise ValueError("Type cannot be None")
        self._type = type
        if form_strategy is None:
            raise ValueError("Form strategy cannot be None")
        self._form_strategy = form_strategy

    @override
    def render(self, *args, **kwargs) -> None:
        # Title
        st.title(self._get_title())

        # Creation
        self._form_strategy.render_form(model=None, form_key="create", *args, **kwargs)

        model = self._form_strategy.get_model(form_key="create")
        if model:
            self._CrudService.create_item(model)
            st.success(f"{self._type.__name__} created successfully!")
            self._form_strategy.clear_form(form_key="create")

        # View
        st.subheader(self._get_view_subtitle())
        data = self._CrudService.get_items()
        for entry in data:
            st.write(f"Name: {entry.name}, Value: {entry.value}, Description: {entry.description}")


    """
        Template methods.
    """
    def _get_title(self) -> str:
        return f"{self._type.__name__} CRUD Page"

    def _get_create_subtitle(self) -> str:
        return f"Create New {self._type.__name__} Entry"

    def _get_view_subtitle(self) -> str:
        return f"View {self._type.__name__} Entries"