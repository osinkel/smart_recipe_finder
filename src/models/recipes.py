from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Table
from src.database import Base
from src.schemas.recipes import Difficulty

association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("recipes.id")),
    Column("right_id", ForeignKey("ingredients.id")),
)

class RecipeModel(Base):
    __tablename__ = 'recipes'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] 
    ingredients: Mapped[List["IngredientModel"] | None] = relationship(secondary=association_table, back_populates="recipes")
    preparation_instructions: Mapped[str]
    cooking_time: Mapped[int]
    difficulty: Mapped[Difficulty]
    cuisine_id: Mapped[int | None] = mapped_column(ForeignKey('cuisines.id'))