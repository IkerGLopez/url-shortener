from src.backend.application.use_cases import RedirectAndTrackUseCase, ShortenUrlUseCase, GetUrlStatsUseCase
from src.backend.infrastructure.adapters.in_memory_repo import Dictionary
from src.backend.infrastructure.adapters.sqlite_repo import SQLite
from src.backend.infrastructure.adapters.routers.api import app, get_shorten_url_use_case as api_get_shorten_url, get_redirect_and_track_use_case as api_get_redirect_and_track, get_show_stats_by_use_case as api_get_show_stats

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

def get_show_stats_by_use_case():
    return GetUrlStatsUseCase(get_repository())

app.dependency_overrides[api_get_shorten_url] = get_shorten_url_use_case
app.dependency_overrides[api_get_redirect_and_track] = get_redirect_and_track_use_case
app.dependency_overrides[api_get_show_stats] = get_show_stats_by_use_case