from src.application.use_cases import RedirectAndTrackUseCase, ShortenUrlUseCase
from src.infrastructure.adapters.in_memory_repo import Dictionary
from src.infrastructure.adapters.sqlite_repo import SQLite
from src.infrastructure.adapters.routers.api import app, get_shorten_url_use_case as api_get_shorten_url, get_redirect_and_track_use_case as api_get_redirect_and_track

USE_SQLITE = True

def get_repository():
    if USE_SQLITE:
        return SQLite("url_shortener.db")
    else:
        return Dictionary()

def get_shorten_url_use_case():
    return ShortenUrlUseCase(get_repository())

def get_redirect_and_track_use_case():
    return RedirectAndTrackUseCase(get_repository())

app.dependency_overrides[api_get_shorten_url] = get_shorten_url_use_case
app.dependency_overrides[api_get_redirect_and_track] = get_redirect_and_track_use_case