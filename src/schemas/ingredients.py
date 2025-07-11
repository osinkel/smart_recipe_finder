from pydantic import BaseModel
from src.schemas.responses import BaseResponse

class IngredientSchema(BaseModel):
    name: str

class IngredientPostSchema(BaseModel):
    id: int
    name: str

class IngredientSuccessResponse(BaseResponse):
    result: IngredientPostSchema