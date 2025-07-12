import pytest
from tests.data import data_to_add, data_to_get, data_to_update

@pytest.mark.parametrize("data, expected_status_code", data_to_add)
@pytest.mark.asyncio(loop_scope="session")
async def test_add_recipe(client, data: dict, expected_status_code: int) -> None:

    response = await client.post("/recipes", json=data)
    assert response.status_code == expected_status_code
    data = response.json()

    if response.status_code == 200:
        assert data['status'] == "success"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_recipe(client) -> None:
    response = await client.post("/recipes", json=data_to_get)
    data = response.json()['result'] 

    response = await client.get(f"/recipes/{data['id']}")
    result = response.json()['result'] 

    assert response.status_code == 200
    assert data['title'] == result['title']
    assert data['id'] == result['id']
    assert data['cooking_time'] == result['cooking_time']
    assert data['preparation_instructions'] == result['preparation_instructions']
    assert data['difficulty'] == result['difficulty']
    assert data['cuisine'] == result['cuisine'] 


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_recipe(client) -> None:
    response = await client.post("/recipes", json=data_to_get)
    data = response.json()['result'] 

    response = await client.delete(f"/recipes/{data['id']}")
    result = response.json() 

    assert response.status_code == 200
    assert result['status'] == 'success'


@pytest.mark.parametrize("recipe, upd_recipe, expected_status_code", data_to_update)
@pytest.mark.asyncio(loop_scope="session")
async def test_update_recipe(client, recipe: dict, upd_recipe: dict, expected_status_code: int) -> None:
    response = await client.post("/recipes", json=recipe)
    data = response.json()['result'] 

    response = await client.put(f"/recipes/{data['id']}", json=upd_recipe)
    result = response.json() 

    assert response.status_code == expected_status_code
    
    if response.status_code == 200: 
        assert result['status'] == 'success'
        assert data['id'] == result['result']['id']
        assert upd_recipe['title'] == result['result']['title']
        assert upd_recipe['cooking_time'] == result['result']['cooking_time']
        assert upd_recipe['preparation_instructions'] == result['result']['preparation_instructions']
        assert upd_recipe['difficulty'] == result['result']['difficulty']
        assert upd_recipe['cuisine']['name'] == result['result']['cuisine']['name']