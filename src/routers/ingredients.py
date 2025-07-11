from fastapi import APIRouter
from src.services.ingredients import IngredientService
from src.schemas.ingredients import IngredientSuccessResponse
from src.schemas.responses import ErrorMsg, ErrorResponse, Status
from src.database import Session

router = APIRouter()

@router.get('/ingredients/{id}', tags=['ingredients'], response_model=IngredientSuccessResponse | ErrorResponse)
async def get_ingredients(id: int, session: Session):
    result = await IngredientService(session).get_ingredient_by_id(id)
    if result:
        return IngredientSuccessResponse(status=Status.SUCCESS, result=result)
    else:
        return ErrorResponse(status=Status.ERROR, message=ErrorMsg.BAD_ID)