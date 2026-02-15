from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from sqlmodel import SQLModel

T = TypeVar("T", bound=SQLModel)

class IStreamLitFormStrategy(ABC, Generic[T]):
    """Abstract interface for form strategies."""
    
    @abstractmethod
    def render_form(self, model: T, *args, **kwargs) -> None:
        """Render the form."""
        pass

    @abstractmethod
    def get_model(self, *args, **kwargs) -> T:
        """Get data from the form."""
        pass

    @abstractmethod
    def clear_form(self) -> None:
        """Clear the form fields."""
        pass