from fastapi import APIRouter
from src.services.recipes import RecipeService
from src.database import Session, engine, Base
from src.schemas.recipes import RecipeSchema, RecipeGetSchema, RecipeSuccessResponse
from src.schemas.responses import ErrorMsg, ErrorResponse, Status

router = APIRouter()

@router.post("/setup")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@router.post('/recipes', tags=['recipes'], response_model= RecipeSuccessResponse | ErrorResponse)
async def add_recipe(recipe: RecipeSchema, session: Session):
    result = await RecipeService(session).add_recipe(recipe)
    if result:
      return RecipeSuccessResponse(status=Status.SUCCESS, result=result)
    else:
        return ErrorResponse(status=Status.ERROR, message=ErrorMsg.DB_ERROR)

@router.get('/recipes/{id}', tags=['recipes'],response_model=RecipeSuccessResponse | ErrorResponse)
async def get_recipe(id: int, session: Session):
    result = await RecipeService(session).get_recipe_by_id(id)
    if result:
        return RecipeSuccessResponse(status=Status.SUCCESS, result=result)
    else:
        return ErrorResponse(status=Status.ERROR, message=ErrorMsg.BAD_ID)

@router.delete('/recipes/{id}', tags=['recipes'],response_model= RecipeSuccessResponse| ErrorResponse)
async def delete_recipe(id: int, session: Session):
    result = await RecipeService(session).delete_recipe_by_id(id)
    if result:
        return RecipeSuccessResponse(status=Status.SUCCESS, result=result)
    else:
        return ErrorResponse(status=Status.ERROR, message=ErrorMsg.BAD_ID)

@router.put('/recipes/{id}', tags=['recipes'],response_model= RecipeSuccessResponse| ErrorResponse)
async def update_recipe(id: int, new_recipe: RecipeSchema, session: Session):
    result = await RecipeService(session).update_recipe_by_id(id, new_recipe)
    if result:
        return RecipeSuccessResponse(status=Status.SUCCESS, result=result)
    else:
        return ErrorResponse(status=Status.ERROR, message=ErrorMsg.BAD_ID)

