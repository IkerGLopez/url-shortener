class InvalidUrlError(Exception):
    def __init__(self, url: str):
        super().__init__(f"NEXT URL IS INVALID: {url}")

class UrlNotFoundError(Exception):
    def __init__(self, code: str):
        super().__init__(f"NEXT SHORTEN CODE DOES NOT EXIST: {code}")

class UrlExpiredError(Exception):
    def __init__(self, url):
        super().__init__(f"NEXT URL IS EXPIRED: {url}")