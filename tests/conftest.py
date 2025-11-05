import os
import shutil
import tempfile
import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.api import auth_routes, user_routes, dataset_routes
try:
    from app.api import transaction_routes
except Exception:
    transaction_routes = None


@pytest.fixture(scope="session")
def test_db_url():
    tmp_dir = tempfile.mkdtemp(prefix="evmarket_test_")
    db_path = os.path.join(tmp_dir, "test_evmarket.db")
    url = f"sqlite:///{db_path}"
    yield url
    shutil.rmtree(tmp_dir, ignore_errors=True)


@pytest.fixture(scope="session")
def test_engine_session(test_db_url):
    engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return engine, TestingSessionLocal


@pytest.fixture()
def client(test_engine_session):
    from app.main import app

    engine, TestingSessionLocal = test_engine_session

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # override all routers' get_db
    app.dependency_overrides[auth_routes.get_db] = override_get_db
    app.dependency_overrides[user_routes.get_db] = override_get_db
    app.dependency_overrides[dataset_routes.get_db] = override_get_db
    if transaction_routes:
        app.dependency_overrides[transaction_routes.get_db] = override_get_db

    return TestClient(app)


