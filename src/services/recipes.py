from typing import List
from sqlalchemy import delete, select
from src.models.recipes import RecipeModel
from src.models.ingredients import IngredientModel
from src.services.base import BaseDataManager, BaseService
from src.services.ingredients import  IngredientDataManager
from src.services.cuisines import CuisineDataManager
from src.schemas.recipes import RecipeSchema, RecipeGetSchema
from sqlalchemy.orm import selectinload
from src.schemas.recipes import (
    RecipeSchema, 
    RecipeSuccessDeleteResponse, 
    RecipeSuccessResponse, 
    RecipeListSuccessResponse
    )
from src.schemas.responses import ErrorMsg, ErrorResponse, Status

class RecipeService(BaseService):
    async def add_recipe(self, recipe_schema: RecipeSchema) -> RecipeSuccessResponse | ErrorResponse:

        recipe = await RecipeDataManager(self.session).add_recipe(recipe_schema)
        if recipe:
          result = RecipeGetSchema.model_validate(recipe, from_attributes=True)
          if await self.session_commit():
              return RecipeSuccessResponse(status=Status.SUCCESS, result=result)
          else:
            return ErrorResponse(status=Status.ERROR, message=ErrorMsg.DB_ERROR)
        else:
            return ErrorResponse(status=Status.ERROR, message=ErrorMsg.DB_ERROR)

    async def get_recipe_by_id(self, id: int) -> RecipeSuccessResponse | ErrorResponse:
        recipe = await RecipeDataManager(self.session).get_recipe_by_id(id)
        if recipe:
            return RecipeSuccessResponse(status=Status.SUCCESS, result=RecipeGetSchema.model_validate(recipe, from_attributes=True))
        else:
            return ErrorResponse(status=Status.ERROR, message=ErrorMsg.BAD_ID)
    
    async def delete_recipe_by_id(self, id: int) -> RecipeSuccessDeleteResponse | ErrorResponse:
        result = await RecipeDataManager(self.session).delete_recipe_by_id(id)  
        if result:
            response = RecipeSuccessDeleteResponse(status=Status.SUCCESS, result=result)
            if await self.session_commit():
                return response
            else:
                response.result = False
                return response
        else:
            return ErrorResponse(status=Status.ERROR, message=ErrorMsg.BAD_ID)
        

    async def update_recipe_by_id(self, id: int, new_recipe: RecipeSchema) -> RecipeSuccessResponse | ErrorResponse:
        recipe = await RecipeDataManager(self.session).update_recipe(id, new_recipe)
        if not recipe:
            return ErrorResponse(status=Status.ERROR, message=ErrorMsg.BAD_ID)
        else:
            recipe = RecipeGetSchema.model_validate(recipe, from_attributes=True)
            if await self.session_commit():
                return RecipeSuccessResponse(status=Status.SUCCESS, result=recipe)
            else:
                return ErrorResponse(status=Status.ERROR, message=ErrorMsg.DB_ERROR)
            
    async def filter_recipes_by_ingredients(self, include: List[str], exclude: List[str]) -> RecipeListSuccessResponse:

        recipes = await RecipeDataManager(self.session).filter_recipes_by_ingredients(include, exclude)
        result = RecipeListSuccessResponse(status=Status.SUCCESS)
        
        if recipes:
            result.result = [RecipeGetSchema.model_validate(recipe, from_attributes=True) for recipe in recipes]

        return result


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

        new_recipe.cuisine = cuisine
        new_recipe.ingredients = ingredients

        await self.add_one(new_recipe)
        return new_recipe
    
    async def get_recipe_by_id(self, id: int) -> RecipeModel | None:
        query = select(RecipeModel).options(selectinload(RecipeModel.ingredients), selectinload(RecipeModel.cuisine)).where(RecipeModel.id == id)
        model = await self.get_one(query)
        return model
    
    async def delete_recipe_by_id(self, id: int) -> RecipeModel | None:
        query = delete(RecipeModel).where(RecipeModel.id == id)
        result = await self.execute(query)  
        return bool(result.rowcount)
    
    async def update_recipe(self, id: int, new_recipe: RecipeSchema) -> RecipeGetSchema | None:

        old_recipe = await self.get_recipe_by_id(id)

        if not old_recipe:
            return None
        
        ingr_names = [ingr.name for ingr in new_recipe.ingredients]
        new_ingredients = await IngredientDataManager(self.session).get_or_add_ingredients_by_name(old_recipe, ingr_names)
        new_cuisine = await CuisineDataManager(self.session).get_or_add_cuisine_by_name(new_recipe.cuisine.name)

        old_recipe.title = new_recipe.title
        old_recipe.preparation_instructions = new_recipe.preparation_instructions
        old_recipe.cooking_time = new_recipe.cooking_time
        old_recipe.difficulty = new_recipe.difficulty
        old_recipe.ingredients = new_ingredients
        old_recipe.cuisine = new_cuisine
        
        await self.add_one(old_recipe)

        return old_recipe
    
    async def filter_recipes_by_ingredients(self, include: List[str], exclude: List[str]) -> List[RecipeModel]:
        query = select(RecipeModel).options(selectinload(RecipeModel.ingredients), selectinload(RecipeModel.cuisine))
        if include:
            query = query.join(RecipeModel.ingredients).filter(IngredientModel.name.in_(include))

        recipes_include = await self.get_all(query)

        recipes_exclude = []

        if exclude:
            query = select(RecipeModel).options(selectinload(RecipeModel.ingredients), selectinload(RecipeModel.cuisine)).join(RecipeModel.ingredients).filter(IngredientModel.name.in_(exclude))
            recipes_exclude = await self.get_all(query)

        recipes = list(set(recipe for recipe in recipes_include if not recipe in recipes_exclude))

        return recipes

        