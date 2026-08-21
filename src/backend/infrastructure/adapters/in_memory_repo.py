from src.backend.application.ports.repositories import IUrlRepository
from src.backend.domain.models import URL

class Dictionary(IUrlRepository):
    def __init__(self):
            self._db: dict[str, URL] = {}
    
    def save(self, url: URL) -> None:
        self._db[url.short_code] = url

    def get_by_code(self, code) -> URL | None:
        return self._db.get(code)