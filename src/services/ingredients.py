from typing import Any, List
from src.models.ingredients import IngredientModel
from sqlalchemy import select
from src.services.base import BaseDataManager, BaseService
from src.schemas.ingredients import IngredientPostSchema, IngredientSchema
from src.models.recipes import RecipeModel

class IngredientService(BaseService):
    async def get_ingredient_by_id(self, id: id) -> IngredientPostSchema:
        model = await IngredientDataManager(self.session).get_ingredient_by_prop(id, "id")
        return IngredientPostSchema.model_validate(model, from_attributes=True) if model else None

    async def add_many_ingredients(self, ingredients: List[str]) -> List[IngredientPostSchema]:
        models = await IngredientDataManager(self.session).add_many_ingredients(ingredients)
        result_schemas = [IngredientPostSchema.model_validate(model, from_attributes=True) for model in models]
        return result_schemas if await self.session_commit() else []

class IngredientDataManager(BaseDataManager):

    async def get_ingredients_by_prop(self, list_val: List[Any], prop: str) -> List[IngredientModel]:
        query = select(IngredientModel).where(getattr(IngredientModel, prop).in_(list_val))
        models = await self.get_all(query)
        return models

    async def get_ingredient_by_prop(self, val: Any, prop: str) -> List[IngredientModel]:
        query = select(IngredientModel).where(getattr(IngredientModel, prop) == val)
        models = await self.get_one(query)
        return models

    async def add_many_ingredients(self, recipe: RecipeModel, ingredients: List[str]) -> List[IngredientModel]:
        new_ingredients = [IngredientModel(name=ingr, recipes=[recipe]) for ingr in ingredients]
        await self.add_all(new_ingredients)
        return new_ingredients
    
    async def get_or_add_ingredients_by_name(self, recipe: RecipeModel, list_names: List[str]) -> List[IngredientModel]:
        existing_ingredients = await self.get_ingredients_by_prop(list_names, "name")
        existing_ingredients_names = [ingr.name for ingr in existing_ingredients]
        non_existent_ingredients = [name for name in list_names if name not in existing_ingredients_names]
        if non_existent_ingredients:
            existing_ingredients += await self.add_many_ingredients(recipe, non_existent_ingredients)
        return existing_ingredients