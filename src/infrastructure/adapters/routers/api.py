from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from src.application.use_cases import RedirectAndTrackUseCase, ShortenUrlUseCase
from src.domain.exceptions import UrlNotFoundError, UrlExpiredError

app = FastAPI()

class UrlRequest(BaseModel):
    original_url: str

def get_shorten_url_use_case() -> ShortenUrlUseCase:
    raise NotImplementedError("Needs to be configured in config.py")

def get_redirect_and_track_use_case() -> RedirectAndTrackUseCase:
    raise NotImplementedError("Needs to be configured in config.py")

@app.post("/shorten")
def shorten_url(request: UrlRequest, use_case: ShortenUrlUseCase = Depends(get_shorten_url_use_case)):
    url_entity = use_case.execute(request.original_url)

    return {"short_code": url_entity.short_code, "original_url": url_entity.original_url}

@app.get("/{code}")
def redirect_by_code(code: str, use_case: RedirectAndTrackUseCase = Depends(get_redirect_and_track_use_case)):
    try:
        original_url = use_case.execute(code)

        return RedirectResponse(original_url)
    except UrlNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UrlExpiredError as e:
        raise HTTPException(status_code=410, detail=(str(e)))