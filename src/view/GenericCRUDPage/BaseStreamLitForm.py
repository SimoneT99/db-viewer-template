from typing import Generic, Optional, Type, TypeVar, override
from pydantic_core import PydanticUndefined
from sqlmodel import SQLModel
import streamlit as st

#injection
from dependency_injector.wiring import Provide, inject
from src.containers.GenericCRUDPageContainer import GenericCRUDPageContainer

from src.view.GenericCRUDPage.StreamLitFieldDispatcher import IStreamLitField
from src.view.Interfaces.IStreamLitFormStrategy import IStreamLitForm

T = TypeVar("T", bound=SQLModel)


class BaseStreamLitForm(IStreamLitForm[T], Generic[T]):
    """Abstract interface for form strategies."""

    @inject
    def __init__(self, model_class: Type[T], field_renderers: Optional[IStreamLitField] = Provide[GenericCRUDPageContainer.standard_field_builder]):
        if model_class is None:
            raise ValueError("Model class cannot be None")
        self._model_class = model_class
        self._field_renderers = field_renderers


    @override
    def render_form(self, model: Optional[T] = None, form_key: str = "form") -> None:
        with st.form(key=form_key):
            st.subheader(f"{self._model_class.__name__} Form")
            
            form_data = {}
            
            for field_name, field_info in self._model_class.model_fields.items():
                
                # Ottieni il valore di default dal modello esistente o dai metadati del field
                default_value = None
                if model:
                    default_value = getattr(model, field_name, None)  
                elif field_info.default is not None and field_info.default != PydanticUndefined:
                    default_value = field_info.default
                elif field_info.default_factory is not None and field_info.default_factory != PydanticUndefined:
                    default_value = field_info.default_factory()
                
                # Genera label dal nome del field
                label = field_name.replace("_", " ").title()
                widget_key = f"{form_key}_{field_name}"
        
                # Auto-detect tipi base
                try:
                    field_renderer =  self._field_renderers.render_field(label, field_info, default_value, widget_key)
                except ValueError as e:
                    st.warning(str(e))
                    continue  # Salta campi non supportati
                form_data[field_name] = field_renderer
            
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                st.session_state[f"{form_key}_data"] = form_data
                st.session_state[f"{form_key}_submitted"] = True


    @override
    def get_model(self, form_key: str = "form") -> Optional[T]:
        """Get model from session_state AFTER form submission"""
        if st.session_state.get(f"{form_key}_submitted"):
            data = st.session_state.get(f"{form_key}_data")
            if data:
                # Clear submission flag
                st.session_state[f"{form_key}_submitted"] = False
                return self._model_class(**data)
        return None
    
    @override
    def clear_form(self, form_key: str = "form") -> None:
        """Clear form state"""
        st.session_state.pop(f"{form_key}_data", None)
        st.session_state.pop(f"{form_key}_submitted", None)

