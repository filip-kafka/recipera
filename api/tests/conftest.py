import pytest
from fastapi.testclient import TestClient
from recipera_api.config import get_settings
from recipera_api.db import models  # noqa: F401
from recipera_api.db.base import Base
from recipera_api.db.session import get_db
from recipera_api.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

settings = get_settings()


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(settings.test_database_url)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
