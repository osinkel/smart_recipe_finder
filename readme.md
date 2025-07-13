
# Smart Recipe Finder


This is back-end part of Smart Recipe Finder application that is used to store, search, and retrieve recipes efficiently with natural language queries. 

Service have RESTful API structure, uses PostgreSQL as database. All request and most important methods covered by test.

## Tech

 - FastAPI
 - PostgreSQL (+Pgvector)
 - SQLAlchemy
 - Pydantic
 - Langchain
 - HuggingFace (sentence-transformers/all-mpnet-base-v2)
 - Docker
 - Pytest

## Features
 - CRUD operations for recipes having the following attributes:
   - title
   - list of ingredients
   - preparation instructions
   - cooking time in minutes
   - difficulty (easy, medium, hard)
   - cuisine (Italian, French, etc.)
   - anything else you consider useful
 - Filtering recipes by ingredients using query parameters, supporting both inclusion and exclusion modes, for example:
   - recipes that include potato, butter, milk, but exclude eggs
   - recipes that exclude onions
 - Natural language search, for example:
   - Quick Italian recipes under 30 minutes”
   - "Vegetarian recipes using potatoes and cheese”
   - “What can I cook with eggs and flour?”
   - “Healthy lunches with avocado”
   - “Recipes for beginner cooks”

## Docker-compose running instructions

For correct running should be file with environment variables. There is attached .env file for test running

```sh
docker-compose up
```

### I highly recommend using local run without (docker-compose)
Because of natural language search uses ML model (HuggingFace)  the service has quite heavy libraries that will not allow you to successfully launch the build in a short time. On my computer it was more than 3000 seconds

## Local running instructions (without docker-compose)

 1. First, you need to install requierments

 
 ```sh
pip install -r requirements.txt
```
 2. Second, you need run PostgreSQL container 

 
 ```sh
docker run --name pgvector-container -e POSTGRES_USER=langchain -e POSTGRES_PASSWORD=langchain -e POSTGRES_DB=langchain -p 5432:5432 -d pgvector/pgvector:pg16
```
 3. Then, in .env file uncomment POSTGRES_HOST variable for local running and to commit for docker running

 4. Run main.py from root directory
```sh
uvicorn src.main:app --reload
```

## Running tests

1. API tests

```sh
python -m pytest tests/api/test_recipes.py
```
2. CRUD tests
```sh
python -m pytest tests/crud/test_recipes.py
```