from abc import ABC, abstractmethod
from src.backend.domain.models import URL

class IUrlRepository(ABC):
    @abstractmethod
    def save(self, url: URL) -> None:
        """Save an URL"""
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> URL | None:
        """Get an URL by its code"""
        pass