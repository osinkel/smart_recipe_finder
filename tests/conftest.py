import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from src.main import app
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import config

engine = create_async_engine(config.db_url_test)

new_async_session = async_sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass

async def get_session():
    async with new_async_session() as session:
        yield session

@pytest_asyncio.fixture(loop_scope="session")
async def session():
    async for session in get_session():
        yield session

@pytest_asyncio.fixture(loop_scope="session")
async def client():

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client