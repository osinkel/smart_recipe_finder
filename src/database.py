from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.config import config

engine = create_async_engine(config.db_url, echo=True)

new_async_session = async_sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass

async def get_session():
    async with new_async_session() as session:
        yield session

