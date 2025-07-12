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

config.db_url = f'postgresql+asyncpg://{config.postgres_user}:{config.postgres_password}@{config.postgres_host}:{config.postgres_port}/{config.postgres_name}'
config.db_url_test = f'postgresql+asyncpg://{config.postgres_user}:{config.postgres_password}@{config.postgres_host}:{config.postgres_port}/{config.postgres_name_test}'

FORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s: %(lineno)d - %(message)s"

logger = logging.getLogger('python-logger')
formatter = logging.Formatter(FORMAT)
logger.setLevel(logging.DEBUG)

stdout_handler = logging.StreamHandler(sys.stdout)

logger.addHandler(stdout_handler)

logger = logging.LoggerAdapter(logger)

# HOST = os.getenv('HOST', '0.0.0.0')
# POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
# USER = os.getenv('POSTGRES_USER', 'postgres')
# PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
# POSTGRES_NAME = os.getenv('POSTGRES_DB', 'postgres')
# POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)
# HTTP_PORT = os.getenv('HTTP_PORT', 8080)

# URL_DB = f'postgresql://{USER}:{PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}'