from typing import Generator

from recipera_api.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

_settings = get_settings()
_engine = create_engine(_settings.database_url, echo=_settings.db_echo)
SessionLocal = sessionmaker(bind=_engine)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
