import logging
import os

from pydantic_settings import BaseSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

current_directory = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    app_name: str = "{{ cookiecutter.project_name }}"
    database_url: str
    storage_path: str


class TestSettings(Settings):
    stage: str = "test"
    database_url: str = ""


class DevSettings(Settings):
    stage: str = "dev"
    database_url: str = "sqlite:///database.db"
    storage_path: str = os.path.abspath(
        os.path.join(
            current_directory,
            "../photos",
        )
    )


class ProdSettings(Settings):
    stage: str = "prod"
    database_url: str = ""


stage = os.environ.get("BE_STAGE", "dev")
if stage == "test":
    logger.info("Loading TestSettings")
    raise (Exception("Test stage not yet configured"))
    settings = TestSettings()
elif stage == "dev":
    logger.info("Loading DevSettings")
    settings = DevSettings()
elif stage == "prod":
    logger.info("Loading ProdSettings")
    raise (Exception("Prod stage not yet configured"))
    settings = ProdSettings()
