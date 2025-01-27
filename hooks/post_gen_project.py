import os

from jinja2 import Environment, FileSystemLoader

env = Environment()

init_content = """
{% raw %}
{% endraw %}
"""

model_content = """
{% raw %}
from sqlmodel import SQLModel, Field, Relationship

###{{ "#" * model|length }}####
## {{ model|title }}s ##
###{{ "#" * model|length }}####


class {{ model|title }}Base(SQLModel):
    name: str = Field(index=True)


class {{ model|title }}({{ model|title }}Base, table=True):
    id: int | None = Field(default=None, primary_key=True)


class {{ model|title }}Public({{ model|title }}Base):
    id: int


class {{ model|title }}Create({{ model|title }}Base):
    pass


class {{ model|title }}Update({{ model|title }}Base):
    name: str | None = None
{% endraw %}
"""

route_content = """
{% raw %}
import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select
from app.db import SessionDep
from app.models.{{ model }}.model import (
    {{ model|title }},
    {{ model|title }}Public,
    {{ model|title }}Create,
    {{ model|title }}Update,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/{{ model }}s")


############
## Create ##
############

@router.post("", response_model={{ model|title }}Public, status_code=status.HTTP_201_CREATED)
def create({{ model }}: {{ model|title }}Create, session: SessionDep):
    logger.debug("Request to POST {{ model|title }} with { {{ model }} }")
    db_{{ model }} = {{ model|title }}.model_validate({{ model }})
    session.add(db_{{ model }})
    session.commit()
    session.refresh(db_{{ model }})
    return db_{{ model }}


##############
## Retrieve ##
##############

@router.get("", response_model=list[{{ model|title }}Public])
def get_plural(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    logger.debug("Request to GET {{ model|title }}s")
    {{ model }}s = session.exec(select({{ model|title }}).offset(offset).limit(limit)).all()
    return {{ model }}s


@router.get("/{ {{ model }}_id }")
def get_singular({{ model }}_id: int, session: SessionDep):
    logger.debug(f"Request to GET {{ model|title }} { {{ model }}_id }")
    {{ model }} = session.get({{ model|title }}, {{ model }}_id)
    if not {{ model }}:
        raise HTTPException(status_code=404, detail="{{ model|title }} not found")
    logger.info(f"{{ model|title }} { {{ model }}_id }: { {{ model }} }")
    return {{ model }}


############
## Update ##
############

@router.patch("/{ {{ model }}_id }", response_model={{ model|title }}Public)
def update({{ model }}_id: int, {{ model }}: {{ model|title }}Update, session: SessionDep):
    logger.debug(f"Request to PATCH {{ model|title }} { {{ model }}_id } with { {{ model }} }")
    db_{{ model }} = session.get({{ model|title }}, {{ model }}_id)
    if not db_{{ model }}:
        raise HTTPException(status_code=404, detail="{{ model|title }} not found")
    {{ model }}_data = {{ model }}.model_dump(exclude_unset=True)
    db_{{ model }}.sqlmodel_update({{ model }}_data)
    session.add(db_{{ model }})
    session.commit()
    session.refresh(db_{{ model }})
    return db_{{ model }}


############
## Delete ##
############

@router.delete("/{ {{ model }}_id }")
def delete({{ model }}_id: int, session: SessionDep):
    logger.debug(f"Request to DELETE {{ model|title }} { {{ model }}_id }")
    db_{{ model }} = session.get({{ model|title }}, {{ model }}_id)
    if not db_{{ model }}:
        raise HTTPException(status_code=404, detail="{{ model|title }} not found")
    session.delete(db_{{ model }})
    session.commit()
    return {"message": f"{{ model|title }} { {{ model }}_id } was deleted."}

{% endraw %}
"""


contents = {
    "__init__.py": init_content,
    "model.py": model_content,
    "route.py": route_content,
}


def write_model_files():
    models = {{cookiecutter.models.list}}
    file_names = contents.keys()

    for model in models:
        # print(f"Processing {model}")
        model_folder = f"services/be/app/models/{model}"
        # create model folder
        os.mkdir(model_folder)
        # create model files
        data = {
            "model": model,
        }
        for file_name in file_names:
            # print(f"Processing {model}-{file_name}")
            with open(f"{model_folder}/{file_name}", "w") as f_obj:
                # template = env.get_template(f"{file_name}.jinja")
                template = env.from_string(contents[file_name])
                # print(f"template={template}")
                rendered_file = template.render(data)
                # print(f"rendered_file={rendered_file}")
                f_obj.write(rendered_file)


if __name__ == "__main__":
    # print("Gonna do post stuff")
    write_model_files()
