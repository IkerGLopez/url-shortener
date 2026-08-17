from datetime import datetime
from src.application.ports.repositories import IUrlRepository
from src.domain.exceptions import UrlNotFoundError
from src.domain.models import URL
from src.domain.services import generate_alias

class ShortenUrlUseCase:
    def __init__(self, repository: IUrlRepository):
        self.repository = repository

    def execute(self, original_url: str) -> URL:
        alias: str = generate_alias(original_url)
        url: URL = URL(original_url, alias, datetime.now(), 0)
        self.repository.save(url)

        return url

class RedirectAndTrackUseCase:
    def __init__(self, repository: IUrlRepository):
        self.repository = repository

    def execute(self, code: str):
        url: URL = self.repository.get_by_code(code)
        if not url:
            raise UrlNotFoundError(code)

        url.click_count += 1
        self.repository.save(url)

        return url.original_url