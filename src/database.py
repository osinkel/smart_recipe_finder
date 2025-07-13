from sqlalchemy import text
from src.config import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.config import config

engine = create_async_engine(config.db_url)

new_async_session = async_sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass


async def init_db():
    async with engine.begin() as conn:

        try:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            logger.info("pgvector extension created or already exists.")
        except Exception as e:
            logger.error(f"Error creating pgvector extension: {e}")


        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with new_async_session() as session:
        yield session

