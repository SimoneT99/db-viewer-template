from typing import Any, Optional, override
from pydantic.fields import FieldInfo
import streamlit as st

"""
   This could be done better, but it's only for the base CRUD Page.
   It's advised to implement the forms and pages for each model of your app.

"""
from abc import ABC, abstractmethod


class IStreamLitField(ABC):
    """Interface for StreamLit form strategies."""

    @abstractmethod
    def render_field(self, label: str, field_info: FieldInfo, default_value: Optional[Any], widget_key: str) -> str:
        """Render the StreamLit form."""
        pass


class StreamLitFieldDispatcher(IStreamLitField):
    """Dispatcher for StreamLit form fields."""

    def __init__(self, dispatcher: dict[type, IStreamLitField]):
        if dispatcher is None:
            raise ValueError("Dispatcher cannot be None")
        self._dispatcher = dispatcher

    @override
    def render_field(self, label: str, field_info: FieldInfo, default_value: Optional[Any], widget_key: str) -> str:
        field_renderer = self._dispatcher.get(field_info.annotation)
        if not field_renderer:
            raise ValueError(f"No field renderer found for type: {field_info.annotation}") if not field_renderer else None
        return field_renderer.render_field(label, field_info, default_value, widget_key)


class TextFieldRenderer(IStreamLitField):

    @override
    def render_field(self, label: str, field_info: FieldInfo, default_value: Optional[Any], widget_key: str) -> str:
        return st.text_input(label, value=default_value or "", key=widget_key, help=field_info.description)

class IntegerFieldRenderer(IStreamLitField):

    @override
    def render_field(self, label: str, field_info: FieldInfo, default_value: Optional[Any], widget_key: str) -> int:
        return st.number_input(label, value=default_value if default_value is not None else 0, step=1, key=widget_key, help=field_info.description)


class FloatFieldRenderer(IStreamLitField):

    @override
    def render_field(self, label: str, field_info: FieldInfo, default_value: Optional[Any], widget_key: str) -> float:
        return st.number_input(label, value=default_value if default_value is not None else 0.0, step=0.1, key=widget_key, help=field_info.description)


class BooleanFieldRenderer(IStreamLitField):

    @override
    def render_field(self, label: str, field_info: FieldInfo, default_value: Optional[Any], widget_key: str) -> bool:
        return st.checkbox(label, value=default_value if default_value is not None else False, key=widget_key, help=field_info.description)
