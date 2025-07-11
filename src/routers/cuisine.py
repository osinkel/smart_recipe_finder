from fastapi import APIRouter
from src.services.cuisines import CuisineService
from src.schemas.cuisines import CuisineSuccessResponse
from src.schemas.responses import ErrorResponse, Status, ErrorMsg
from src.database import Session

router = APIRouter()

@router.get('/cuisines/{id}', tags=['cuisines'], response_model= CuisineSuccessResponse | ErrorResponse)
async def get_cuisine(id: int, session: Session):
    result = await CuisineService(session).get_cuisine_by_id(id)
    if result:
        return CuisineSuccessResponse(status=Status.SUCCESS, result=result)
    else:
        return ErrorResponse(status=Status.ERROR, message=ErrorMsg.BAD_ID)