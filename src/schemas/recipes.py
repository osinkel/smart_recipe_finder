from enum import Enum
from pydantic import BaseModel
from src.schemas.ingredients import IngredientSchema, IngredientPostSchema
from src.schemas.cuisines import CuisineSchema, CuisinePostSchema
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
    ingredients: list[IngredientPostSchema]
    preparation_instructions: str
    cooking_time: int
    difficulty: Difficulty
    cuisine: CuisinePostSchema

class RecipeSuccessResponse(BaseResponse):
    result: RecipeGetSchema