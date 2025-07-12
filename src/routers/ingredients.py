from typing import List
from fastapi import APIRouter
from src.services.ingredients import IngredientService
from src.schemas.ingredients import IngredientSuccessResponse, IngredientsSuccessResponse, IngredientSchema
from src.schemas.responses import ErrorResponse
from src.routers.dependencies import Session

router = APIRouter()

@router.get('/ingredients/{id}', tags=['ingredients'], response_model=IngredientSuccessResponse | ErrorResponse)
async def get_ingredient(id: int, session: Session):
    return await IngredientService(session).get_ingredient_by_id(id)