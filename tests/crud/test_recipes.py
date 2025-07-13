from typing import Dict, List
import pytest
from services.recipes import RecipeService
from src.routers.dependencies import Session
from src.schemas.recipes import RecipeSchema
from tests.data import data_to_get, data_to_filter, data_to_search_similarity
from src.schemas.responses import Status


@pytest.mark.asyncio(loop_scope="session")
async def test_add_recipe(session: Session):
    schema = RecipeSchema.model_validate(data_to_get)
    recipe = await RecipeService(session).add_recipe(schema)
    assert Status.SUCCESS == recipe.status
    assert schema.title == recipe.result.title
    assert schema.cooking_time == recipe.result.cooking_time
    assert schema.preparation_instructions == recipe.result.preparation_instructions
    assert schema.difficulty == recipe.result.difficulty
    assert schema.cuisine.name ==recipe.result.cuisine.name


@pytest.mark.asyncio(loop_scope="session")
async def test_get_recipe(session: Session):
    schema = RecipeSchema.model_validate(data_to_get)
    recipe = await RecipeService(session).add_recipe(schema)
    recipe2 = await RecipeService(session).get_recipe_by_id(recipe.result.id)
    assert recipe2.status == Status.SUCCESS
    assert recipe2.result.title == recipe.result.title
    assert recipe2.result.cooking_time == recipe.result.cooking_time
    assert recipe2.result.preparation_instructions == recipe.result.preparation_instructions
    assert recipe2.result.difficulty == recipe.result.difficulty
    assert recipe2.result.cuisine.name ==recipe.result.cuisine.name


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_recipe(session: Session):
    schema = RecipeSchema.model_validate(data_to_get)
    recipe = await RecipeService(session).add_recipe(schema)
    result = await RecipeService(session).delete_recipe_by_id(recipe.result.id)
    
    assert result.result == True
    assert result.status == Status.SUCCESS

@pytest.mark.asyncio(loop_scope="session")
async def test_update_recipe(session: Session):
    schema = RecipeSchema.model_validate(data_to_get)
    recipe = await RecipeService(session).add_recipe(schema)

    schema.title = 'new_title'
    schema.cooking_time = 10000
    schema.preparation_instructions = 'new_prep_instr'

    recipe2 = await RecipeService(session).update_recipe_by_id(recipe.result.id, schema)
    
    assert recipe2.status == Status.SUCCESS
    assert recipe2.result.title == schema.title
    assert recipe2.result.cooking_time == schema.cooking_time
    assert recipe2.result.preparation_instructions == schema.preparation_instructions
    assert recipe2.result.difficulty == schema.difficulty
    assert recipe2.result.cuisine.name ==schema.cuisine.name

@pytest.mark.parametrize("recipes, filters", data_to_filter)
@pytest.mark.asyncio(loop_scope="session")
async def test_recipe_filter(session: Session, recipes: List[Dict], filters: List[Dict]) -> None:

    for recipe in recipes:
        await RecipeService(session).add_recipe(RecipeSchema.model_validate(recipe))

    for filter in filters:
        result = await RecipeService(session).filter_recipes_by_ingredients(filter['include'], filter['exclude'])

        assert result.status == Status.SUCCESS

        for recipe in result.result:
            ingredients = [ingr.name for ingr in recipe.ingredients]

            for include in filter['include']:
                assert include in ingredients

            for exclude in filter['exclude']:
                assert exclude not in ingredients