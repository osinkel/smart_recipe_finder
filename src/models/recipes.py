from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Table
from src.database import Base
from src.schemas.recipes import Difficulty

association_table = Table(
    "recipes_ingredients_table",
    Base.metadata,
    Column("recipe_id", ForeignKey("recipes.id", ondelete="CASCADE")),
    Column("ingredient_id", ForeignKey("ingredients.id", ondelete="CASCADE")),
)

class RecipeModel(Base):
    __tablename__ = 'recipes'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] 
    ingredients: Mapped[List["IngredientModel"] | None] = relationship(secondary=association_table, back_populates="recipes", passive_deletes=True)
    preparation_instructions: Mapped[str]
    cooking_time: Mapped[int]
    difficulty: Mapped[Difficulty]
    cuisine_id: Mapped[int | None] = mapped_column(ForeignKey('cuisines.id'))
    cuisine: Mapped["CuisineModel"] = relationship(back_populates="recipes")