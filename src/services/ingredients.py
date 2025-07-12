from typing import Any, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.services.base import BaseDataManager, BaseService
from src.schemas.ingredients import IngredientGetSchema
from src.models.ingredients import IngredientModel
from src.models.recipes import RecipeModel
from src.schemas.ingredients import IngredientSuccessResponse, IngredientsSuccessResponse, IngredientSchema
from src.schemas.responses import ErrorMsg, ErrorResponse, Status

class IngredientService(BaseService):
    async def get_ingredient_by_id(self, id: id) -> IngredientSuccessResponse | ErrorResponse:
        model = await IngredientDataManager(self.session).get_ingredient_by_prop(id, "id")
        
        if model:
            return IngredientSuccessResponse(status=Status.SUCCESS, result=IngredientGetSchema.model_validate(model, from_attributes=True))
        else:
            return ErrorResponse(status=Status.ERROR, message=ErrorMsg.BAD_ID)

class IngredientDataManager(BaseDataManager):

    async def get_ingredients_by_prop(self, list_val: List[Any], prop: str) -> List[IngredientModel]:
        query = select(IngredientModel).options(selectinload(IngredientModel.recipes)).where(getattr(IngredientModel, prop).in_(list_val))
        models = await self.get_all(query)
        return models

    async def get_ingredient_by_prop(self, val: Any, prop: str) -> List[IngredientModel]:
        query = select(IngredientModel).options(selectinload(IngredientModel.recipes)).where(getattr(IngredientModel, prop) == val)
        models = await self.get_one(query)
        return models

    async def add_many_ingredients(self, recipe: RecipeModel | None, ingredients: List[str]) -> List[IngredientModel]:
        if recipe:
            new_ingredients = [IngredientModel(name=ingr, recipes=[recipe]) for ingr in ingredients]
        else: 
            new_ingredients = [IngredientModel(name=ingr) for ingr in ingredients]

        await self.add_all(new_ingredients)
        return new_ingredients
    
    async def get_or_add_ingredients_by_name(self, recipe: RecipeModel, list_names: List[str]) -> List[IngredientModel]:
        existing_ingredients = await self.get_ingredients_by_prop(list_names, "name")
        existing_ingredients_names = [ingr.name for ingr in existing_ingredients]
        non_existent_ingredients = [name for name in list_names if name not in existing_ingredients_names]
        if non_existent_ingredients:
            existing_ingredients += await self.add_many_ingredients(recipe, non_existent_ingredients)
        return existing_ingredients