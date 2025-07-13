import logging
import sys
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
        env_file_encoding="utf-8",
    )

    db_url: str = ''
    db_url_test: str = ''

config = Config()

config.db_url = f'postgresql+asyncpg://{config.postgres_user}:{config.postgres_password}@{config.postgres_host}:{config.postgres_port}/{config.postgres_db}'

FORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s: %(lineno)d - %(message)s"

logger = logging.getLogger('python-logger')
formatter = logging.Formatter(FORMAT)
logger.setLevel(logging.DEBUG)

stdout_handler = logging.StreamHandler(sys.stdout)

logger.addHandler(stdout_handler)

logger = logging.LoggerAdapter(logger)