from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from src.schemas.ingredients import IngredientSchema, IngredientGetSchema
from src.schemas.cuisines import CuisineSchema, CuisineGetSchema
from src.schemas.responses import BaseResponse

class Difficulty(Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'

class RecipeSchema(BaseModel):
    title: str
    ingredients: list[IngredientSchema]
    preparation_instructions: str
    cooking_time: int
    difficulty: Difficulty
    cuisine: CuisineSchema

class RecipeGetSchema(BaseModel):
    id: int
    title: str
    ingredients: list[IngredientGetSchema]
    preparation_instructions: str
    cooking_time: int
    difficulty: Difficulty
    cuisine: CuisineGetSchema

class RecipeSuccessResponse(BaseResponse):
    result: RecipeGetSchema

class RecipeListSuccessResponse(BaseResponse):
    result: List[RecipeGetSchema] = Field(default_factory=list)

class RecipeSuccessDeleteResponse(BaseResponse):
    result: bool