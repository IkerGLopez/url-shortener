from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.backend.application.use_cases import RedirectAndTrackUseCase, ShortenUrlUseCase, GetUrlStatsUseCase
from src.backend.domain.exceptions import UrlNotFoundError, UrlExpiredError

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlRequest(BaseModel):
    original_url: str

def get_shorten_url_use_case() -> ShortenUrlUseCase:
    raise NotImplementedError("Needs to be configured in config.py")

def get_redirect_and_track_use_case() -> RedirectAndTrackUseCase:
    raise NotImplementedError("Needs to be configured in config.py")

def get_show_stats_by_use_case() -> GetUrlStatsUseCase:
    raise NotImplementedError("Needs to be configured in config.py")

@app.post("/shorten")
def shorten_url(url_request: UrlRequest, http_request: Request, use_case: ShortenUrlUseCase = Depends(get_shorten_url_use_case)):
    url_entity = use_case.execute(url_request.original_url)
    short_url = f"{http_request.base_url}{url_entity.short_code}"

    return {
            "short_code": url_entity.short_code,
            "original_url": url_entity.original_url,
            "short_url": short_url
        }

@app.get("/{code}")
def redirect_by_code(code: str, use_case: RedirectAndTrackUseCase = Depends(get_redirect_and_track_use_case)):
    try:
        original_url = use_case.execute(code)

        return RedirectResponse(original_url)
    except UrlNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UrlExpiredError as e:
        raise HTTPException(status_code=410, detail=str(e))

@app.get("/stats/{code}")
def show_stats_by_code(code: str, use_case: GetUrlStatsUseCase = Depends(get_show_stats_by_use_case)):
    try:
        url = use_case.execute(code)

        return {
            "original_url": url.original_url,
            "short_code": url.short_code,
            "click_count": url.click_count,
            "expires_at": url.expires_at
                }
    except UrlNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))