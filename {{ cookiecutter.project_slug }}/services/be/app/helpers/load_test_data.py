"""
docker compose exec be poetry run app/helpers/load_test_data.py
"""

from sqlmodel import Session
from app.db import engine, create_db_and_tables, dump_db_and_tables
{% for model in cookiecutter.models %}
from app.models.{{ model }}.model import {{ model|title }}
{% endfor %}


def add_and_commit(obj):
    with Session(engine) as session:
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj


def create_demo_data():
    {% for model in cookiecutter.models %}
    test_data_{{ loop.index }} = add_and_commit(
        {{ model|title }}(
            name="Sample",
        )
    )
    {% endfor %}


def reset_db(with_test_data: bool = False):
    dump_db_and_tables()
    create_db_and_tables()
    if with_test_data:
        create_demo_data()


if __name__ == "__main__":
    create_demo_data()
