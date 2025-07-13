from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends
from src.database import get_session


Session = Annotated[AsyncSession, Depends(get_session)]
