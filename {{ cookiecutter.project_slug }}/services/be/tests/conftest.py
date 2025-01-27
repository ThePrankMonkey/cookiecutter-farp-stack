import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

import sys

sys.path.append(".")

from app.main import app
from app.db import get_session
{% for model in cookiecutter.models.list %}
from app.models.{{ model }}.model import {{ model|title }}
{% endfor %}


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_data")
def test_data_fixture(session: Session):
    """Create test data."""
    {% for model in cookiecutter.models.list %}
    {{ model }}1 = {{ model|title }}(
        name="Test {{ model|title }}",
    )
    {% endfor %}
    {% for model in cookiecutter.models.list %}
    session.add({{ model }}1)
    {% endfor %}
    session.commit()
    {% for model in cookiecutter.models.list %}
    session.refresh({{ model }}1)
    {% endfor %}
    return {
        {% for model in cookiecutter.models.list %}
        "{{ model }}": {{ model }}1,
        {% endfor %}
    }
