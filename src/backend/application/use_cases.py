from datetime import datetime, timedelta
from src.backend.application.ports.repositories import IUrlRepository
from src.backend.domain.exceptions import UrlNotFoundError, UrlExpiredError
from src.backend.domain.models import URL
from src.backend.domain.services import generate_alias

class ShortenUrlUseCase:
    def __init__(self, repository: IUrlRepository):
        self.repository = repository

    def execute(self, original_url: str) -> URL:
        alias: str = generate_alias(original_url)
        now: datetime = datetime.now()
        url: URL = URL(original_url, alias, now, 0, now + timedelta(weeks=1))
        self.repository.save(url)

        return url

class RedirectAndTrackUseCase:
    def __init__(self, repository: IUrlRepository):
        self.repository = repository

    def execute(self, code: str) -> str:
        url: URL = self.repository.get_by_code(code)
        if not url:
            raise UrlNotFoundError(code)

        if datetime.fromisoformat(url.expires_at) < datetime.now():
            raise UrlExpiredError(url.original_url)

        url.click_count += 1
        self.repository.save(url)

        return url.original_url

class GetUrlStatsUseCase:
    def __init__(self, repository: IUrlRepository):
        self.repository = repository

    def execute(self, code: str) -> URL:
        url: URL = self.repository.get_by_code(code)
        if not url:
            raise UrlNotFoundError(code)

        return url