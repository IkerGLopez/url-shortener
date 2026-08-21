from src.backend.application.ports.repositories import IUrlRepository
from src.backend.domain.models import URL
import sqlite3

class SQLite(IUrlRepository):
    def __init__(self, db_path: str):
        self._db = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self._db.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS URL (
                original_url TEXT,
                short_code TEXT PRIMARY KEY,
                created_at TIMESTAMP,
                click_count INTEGER,
                expires_at TIMESTAMP
            )
        """)

    def save(self, url: URL) -> None:
        url_exists = self.get_by_code(url.short_code)

        if not url_exists:
            self.cursor.execute("""
                INSERT INTO URL VALUES(?, ?, ?, ?, ?)
            """,
            (url.original_url, url.short_code, url.created_at, url.click_count, url.expires_at)
            )
        else:
            self.cursor.execute("""
                UPDATE URL SET click_count=?
                WHERE short_code=?
            """,
            (url.click_count, url.short_code)
            )

        self._db.commit()

    def get_by_code(self, code: str) -> URL | None:
        self.cursor.execute("""
            SELECT *
            FROM URL
            WHERE short_code = ?
        """,
        (code,)
        )

        row = self.cursor.fetchone()

        if row:
            return URL(
                original_url=row[0],
                short_code=row[1],
                created_at=row[2],
                click_count=row[3],
                expires_at=row[4]
            )

        return None