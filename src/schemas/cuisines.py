from pydantic import BaseModel
from src.schemas.responses import BaseResponse

class CuisineSchema(BaseModel):
    name: str

class CuisinePostSchema(BaseModel):
    id: int
    name: str

class CuisineGetSchema(CuisineSchema):
    id: int

class CuisineSuccessResponse(BaseResponse):
    result: CuisineGetSchema