from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class IngredientModel(Base):
    __tablename__ = 'ingredients'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] 
    recipes: Mapped[List["RecipeModel"] | None] = relationship(secondary="association_table", back_populates="ingredients")