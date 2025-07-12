from typing import List
from pydantic import BaseModel
from src.schemas.responses import BaseResponse

class IngredientSchema(BaseModel):
    name: str

class IngredientGetSchema(IngredientSchema):
    id: int

class IngredientSuccessResponse(BaseResponse):
    result: IngredientGetSchema

class IngredientsSuccessResponse(BaseResponse):
    result: List[IngredientGetSchema]