from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class CuisineModel(Base):
    __tablename__ = 'cuisines'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    reciepes: Mapped[List['RecipeModel'] | None] = relationship()
