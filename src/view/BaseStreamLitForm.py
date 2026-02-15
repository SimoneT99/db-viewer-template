from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeVar, override
from sqlmodel import SQLModel
import streamlit as st

T = TypeVar("T", bound=SQLModel)

class BaseStreamLitForm(ABC, Generic[T]):
    """Abstract interface for form strategies."""

    def __init__(self, type: Type[T]):
        if type is None:
            raise ValueError("Type cannot be None")
        self._type = type
        self._form_data = {}

    @override
    def render_form(self, model: T, *args, **kwargs) -> None:
        """Render the form dynamically based on the SQLModel fields."""
        for field_name, field_type in self._type.__annotations__.items():
            
            default_value = getattr(model, field_name, None) if model else kwargs.get(field_name, None)
            
            if field_type == str:
                self._form_data[field_name] = st.text_input(field_name, value=default_value or "")
            elif field_type == int:
                self._form_data[field_name] = st.number_input(field_name, value=default_value if default_value is not None else 0, step=1)
            elif field_type == float:
                self._form_data[field_name] = st.number_input(field_name, value=default_value if default_value is not None else 0.0, step=0.1)
            elif field_type == bool:
                self._form_data[field_name] = st.checkbox(field_name, value=default_value if default_value is not None else False)
            else:
                st.warning(f"Field type {field_type} for {field_name} is not supported.")

    @override
    def get_model(self, *args, **kwargs) -> T:
        """Get data from the form and return an instance of the model."""
        model_data = {}
        for field_name in self._form_data:
            model_data[field_name] = self._form_data[field_name]
        return self._type(**model_data)

    @override
    def clear_form(self) -> None:
        """Clear the form fields."""
        self._form_data = {}