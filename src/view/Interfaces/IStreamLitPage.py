from abc import ABC, abstractmethod

class IStreamLitPage(ABC):
    """Abstract interface for StreamLit pages."""
    
    @abstractmethod
    def render(self, *args, **kwargs) -> None:
        """Render the StreamLit page."""
        pass