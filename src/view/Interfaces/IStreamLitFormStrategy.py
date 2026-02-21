from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar
from sqlmodel import SQLModel

T = TypeVar("T", bound=SQLModel)


class IStreamLitForm(ABC, Generic[T]):
    """Interface: Streamlit form rendering abstraction.

    Implementations of this interface provide an abstraction for rendering
    a form for a given SQLModel (Pydantic-based) instance, extracting
    a model from the form after submission, and clearing the form state.
    """

    @abstractmethod
    def render_form(
        self,
        model: Optional[T] = None,
        form_key: str = "form",
        **kwargs,
    ) -> None:
        """Render the Streamlit form for T using the provided model and options.

        Parameters:
        - model: optional initial model used to populate the form fields if not None.
        - form_key: Streamlit widget key or namespace for the form.
        - kwargs: additional implementation-specific options.
        """
        pass

    @abstractmethod
    def get_model(self, form_key: str = "form") -> Optional[T]:
        """Return the model constructed from submitted form values.

        Raises:
        - `pydantic.ValidationError` if submitted values fail model validation.
        """
        pass

    @abstractmethod
    def clear_form(self, form_key: str = "form") -> None:
        """Clear the form state identified by `form_key`.

        Implementations should remove or reset any stored widget state
        so the form appears blank or returns to its initial state.
        """
        pass