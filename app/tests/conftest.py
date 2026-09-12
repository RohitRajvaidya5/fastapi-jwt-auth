
from sqlalchemy import create_engine
from app.database import Base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
import pytest

TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

Base.metadata.create_all(bind=test_engine)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

@pytest.fixture
def override_database(test_db):

    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    yield

    app.dependency_overrides.clear()


@pytest.fixture
def sample_number():
    return 10

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)
