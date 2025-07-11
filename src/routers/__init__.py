from fastapi import APIRouter

from src.routers.recipes import router as recipe_router
from src.routers.cuisine import router as cuisine_router
from src.routers.ingredients import router as ingredients_router

main_router = APIRouter()

main_router.include_router(recipe_router)
main_router.include_router(cuisine_router)
main_router.include_router(ingredients_router)