from typing import Dict, List
from httpx import AsyncClient
import pytest
from tests.data import (
    data_to_add, data_to_get, 
    data_to_update, 
    data_to_filter, 
    data_to_search_similarity)
from src.schemas.recipes import (
    RecipeListSuccessResponse, 
    RecipeSuccessResponse, 
    RecipeSuccessDeleteResponse
    )
from src.schemas.responses import Status

@pytest.mark.parametrize("data, expected_status_code", data_to_add)
@pytest.mark.asyncio(loop_scope="session")
async def test_add_recipe(client: AsyncClient, data: dict, expected_status_code: int) -> None:

    response = await client.post("/recipes", json=data)
    assert response.status_code == expected_status_code

    if response.status_code == 200:
        result = RecipeSuccessResponse.model_validate(response.json())
        assert result.status == Status.SUCCESS


@pytest.mark.asyncio(loop_scope="session")
async def test_get_recipe(client: AsyncClient) -> None:
    response = await client.post("/recipes", json=data_to_get)
    data = RecipeSuccessResponse.model_validate(response.json()) 

    response = await client.get(f"/recipes/{data.result.id}")
    result = RecipeSuccessResponse.model_validate(response.json()) 

    assert response.status_code == 200
    assert result.status == Status.SUCCESS
    assert data.result.id == result.result.id



@pytest.mark.asyncio(loop_scope="session")
async def test_delete_recipe(client: AsyncClient) -> None:
    response = await client.post("/recipes", json=data_to_get)
    data = RecipeSuccessResponse.model_validate(response.json())

    response = await client.delete(f"/recipes/{data.result.id}")

    assert response.status_code == 200
    
    result = RecipeSuccessDeleteResponse.model_validate(response.json()) 

    assert result.status == Status.SUCCESS


@pytest.mark.parametrize("recipe, upd_recipe, expected_status_code", data_to_update)
@pytest.mark.asyncio(loop_scope="session")
async def test_update_recipe(client: AsyncClient, recipe: dict, upd_recipe: dict, expected_status_code: int) -> None:
    response = await client.post("/recipes", json=recipe)
    data = RecipeSuccessResponse.model_validate(response.json()) 

    response = await client.put(f"/recipes/{data.result.id}", json=upd_recipe)

    assert response.status_code == expected_status_code
    
    if response.status_code == 200: 
        result = RecipeSuccessResponse.model_validate(response.json())
        from src.config import logger
        assert result.status == Status.SUCCESS
        assert data.result.id== result.result.id
        assert upd_recipe['title'] == result.result.title
        assert upd_recipe['cooking_time'] == result.result.cooking_time
        assert upd_recipe['preparation_instructions'] == result.result.preparation_instructions
        assert upd_recipe['difficulty'] == result.result.difficulty.value
        assert upd_recipe['cuisine']['name'] == result.result.cuisine.name

@pytest.mark.parametrize("recipes, filters", data_to_filter)
@pytest.mark.asyncio(loop_scope="session")
async def test_recipe_filter(client: AsyncClient, recipes: List[Dict], filters: List[Dict]) -> None:
    for recipe in recipes:
        response = await client.post("/recipes", json=recipe)

    for filter in filters:
        response = await client.get(f"/recipes/filter/", params={'include': filter['include'], 'exclude': filter['exclude']})
        assert response.status_code == filter['expected_status_code']

        result = RecipeListSuccessResponse.model_validate(response.json())

        assert result.status == Status.SUCCESS

        for recipe in result.result:
            ingredients = [ingr.name for ingr in recipe.ingredients]

            for include in filter['include']:
                assert include in ingredients

            for exclude in filter['exclude']:
                assert exclude not in ingredients


@pytest.mark.parametrize("recipes, search_data", data_to_search_similarity)
@pytest.mark.asyncio(loop_scope="session")
async def test_recipe_search_by_content_similarity(client: AsyncClient, recipes: List[Dict], search_data: List[Dict]) -> None:
    await client.post("/setup")
    for recipe in recipes:
        response = await client.post("/recipes", json=recipe)

    for search in search_data:
        response = await client.get(f"/recipes/search/", params={'search_text': search['search_text'], 'limit': search['limit']})
        assert response.status_code == search['expected_status_code']

        result = RecipeListSuccessResponse.model_validate(response.json())

        assert result.status == Status.SUCCESS
        assert result.result[0].title == search['expected_best_recipe']
