from typing import List, Optional
from fastapi import APIRouter, Query
from src.services.recipes import RecipeService
from src.routers.dependencies import Session
from src.database import engine, Base
from src.schemas.recipes import (
    RecipeSchema, 
    RecipeSuccessDeleteResponse, 
    RecipeSuccessResponse, 
    RecipeListSuccessResponse)
from src.schemas.responses import ErrorResponse

router = APIRouter()

@router.post("/setup")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@router.post('/recipes', tags=['recipes'], response_model= RecipeSuccessResponse | ErrorResponse)
async def add_recipe(recipe: RecipeSchema, session: Session):
    return await RecipeService(session).add_recipe(recipe)

@router.get('/recipes/{id}', tags=['recipes'],response_model=RecipeSuccessResponse | ErrorResponse)
async def get_recipe(id: int, session: Session):
    return await RecipeService(session).get_recipe_by_id(id)

@router.get('/recipes/filter/', tags=['recipes'],response_model=RecipeListSuccessResponse | ErrorResponse)
async def filter_recipes_by_ingredients(
    session: Session,
    include: List[str] = Query([]),
    exclude: List[str] = Query([]),
    ):
    return await RecipeService(session).filter_recipes_by_ingredients(include, exclude)

@router.delete('/recipes/{id}', tags=['recipes'],response_model= RecipeSuccessDeleteResponse | ErrorResponse)
async def delete_recipe(id: int, session: Session):
    return await RecipeService(session).delete_recipe_by_id(id)

@router.put('/recipes/{id}', tags=['recipes'],response_model= RecipeSuccessResponse| ErrorResponse)
async def update_recipe(id: int, new_recipe: RecipeSchema, session: Session):
    return await RecipeService(session).update_recipe_by_id(id, new_recipe)

