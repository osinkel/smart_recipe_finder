from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from .config import config
from typing import Annotated
from fastapi import Depends

engine = create_async_engine(config.db_url, echo=True)

new_async_session = async_sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass

async def get_session():
    async with new_async_session() as session:
        yield session

Session = Annotated[AsyncSession, Depends(get_session)]