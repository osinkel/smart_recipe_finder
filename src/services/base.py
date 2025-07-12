import traceback
from typing import Any, List, Sequence
from src.routers.dependencies import Session
from sqlalchemy.sql.expression import Executable
from src.config import logger

class SessionMixin:

    def __init__(self, session: Session) -> None:
        self.session = session

    async def session_commit(self) -> bool:
        is_success = True
        try:
            await self.session.commit()
        except Exception:
            logger.exception(traceback.format_exc())
            is_success = False
            await self.session.rollback()
        return is_success

class BaseService(SessionMixin):
    pass

class BaseDataManager(SessionMixin):

    async def add_one(self, model: Any) -> None:
        self.session.add(model)
        await self.flush()

    async def add_all(self, models: Sequence[Any]) -> None:
        self.session.add_all(models)
        await self.flush()

    async def flush(self) -> None:
        await self.session.flush()

    async def get_one(self, query: Executable) -> Any:
        result = await self.session.execute(query)
        return result.scalar()
    
    async def execute(self, query: Executable, params: dict = None) -> Any:
        return await self.session.execute(query, params)

    async def get_all(self, query: Executable) -> List[Any]:
        result = await self.session.execute(query)
        return list(result.scalars().all())