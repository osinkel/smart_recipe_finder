from typing import List

from sqlalchemy import delete, select
from src.models.recipes import RecipeModel
from src.models.cuisines import CuisineModel
from src.models.ingredients import IngredientModel
from src.services.base import BaseDataManager, BaseService
from src.services.ingredients import IngredientService, IngredientDataManager
from src.services.cuisines import CuisineService, CuisineDataManager
from src.schemas.recipes import RecipeSchema, RecipeGetSchema
from src.schemas.cuisines import CuisinePostSchema
from src.schemas.ingredients import IngredientPostSchema
from pydantic import TypeAdapter 

class RecipeService(BaseService):
    async def add_recipe(self, recipe_schema: RecipeSchema) -> RecipeGetSchema | None:

        recipe = await RecipeDataManager(self.session).add_recipe(recipe_schema)
        result_schema = RecipeGetSchema(
            id=recipe.id,
            title=recipe.title,
            cooking_time=recipe.cooking_time,
            difficulty=recipe.difficulty,
            preparation_instructions=recipe.preparation_instructions,
            ingredients=[IngredientPostSchema.model_validate(model, from_attributes=True) for model in recipe.ingredients],
            cuisine=CuisinePostSchema(id=recipe.cuisine_id, name=recipe_schema.cuisine.name)
        )
        return result_schema if await self.session_commit() else None

    async def get_recipe_by_id(self, id: int) -> RecipeGetSchema | None:
        return await RecipeDataManager(self.session).get_recipe_by_id(id)
    
    async def delete_recipe_by_id(self, id: int) -> bool:
        return await RecipeDataManager(self.session).delete_recipe_by_id(id)  

    async def update_recipe_by_id(self, id: int, new_recipe: RecipeSchema) -> RecipeGetSchema | None:

        old_recipe = await self.get_recipe_by_id(id)

        ingr_names = [ingr.name for ingr in new_recipe.ingredients]
        new_ingredients = await IngredientDataManager(self.session).get_or_add_ingredients_by_name(ingr_names)

        new_cuisine = await CuisineDataManager(self.session).get_or_add_cuisine_by_name(new_recipe.cuisine.name)

        return await RecipeDataManager(self.session).update_recipe(old_recipe, new_recipe, new_ingredients, new_cuisine)


class RecipeDataManager(BaseDataManager):

    async def add_recipe(self, recipe: RecipeSchema) -> RecipeModel | None:
        new_recipe = RecipeModel(
            title=recipe.title,
            preparation_instructions=recipe.preparation_instructions,
            cooking_time=recipe.cooking_time,
            difficulty=recipe.difficulty,
        )
        ingr_names = [ingr.name for ingr in recipe.ingredients]
        ingredients = await IngredientDataManager(self.session).get_or_add_ingredients_by_name(new_recipe, ingr_names)
        cuisine = await CuisineDataManager(self.session).get_or_add_cuisine_by_name(recipe.cuisine.name)

        new_recipe.cuisine_id = cuisine.id
        new_recipe.ingredients = ingredients

        await self.add_one(new_recipe)
        return new_recipe
    
    async def get_recipe_by_id(self, id: int) -> RecipeGetSchema | None:
        query = select(RecipeModel).where(RecipeModel.id == id)
        model = await self.get_one(query)
        return RecipeGetSchema(**model.to_dict()) if model else None
    
    async def delete_recipe_by_id(self, id: int) -> bool:
        model = await self.get_recipe_by_id(id)

        is_deleted = False

        if model:
            model.delete()
            is_deleted = await self.session_commit()

        return is_deleted
    
    async def update_recipe(self, old_recipe: RecipeGetSchema, new_recipe: RecipeModel, new_ingredients: List[IngredientModel], new_cuisine: CuisineModel) -> RecipeGetSchema | None:
        old_recipe.title = new_recipe.title
        old_recipe.preparation_instructions = new_recipe.preparation_instructions
        old_recipe.cooking_time = new_recipe.cooking_time
        old_recipe.difficulty = new_recipe.difficulty
        old_recipe.ingredients = new_ingredients
        old_recipe.cuisine = new_cuisine
       
        model = RecipeModel(**old_recipe.model_dump())
        model.update()

        commit_result = await self.session_commit()

        return RecipeGetSchema(**model.to_dict()) if commit_result else None