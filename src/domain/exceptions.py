class InvalidUrlError(Exception):
    def __init__(self, url: str):
        super().__init__(f"NEXT URL IS INVALID: {url}")

class UrlNotFoundError(Exception):
    def __init__(self, url: str):
        super().__init__(f"NEXT URL DOES NOT EXIST: {url}")