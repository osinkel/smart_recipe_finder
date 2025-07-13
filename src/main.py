from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database import init_db
from src.routers import main_router
from src.config import config
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
   await init_db()
   yield 

app = FastAPI(
    title='Smart recipe finder',
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    lifespan=lifespan
)

app.include_router(main_router)

if __name__ == '__main__': 
    uvicorn.run(app, host=config.host, port=config.port) # uvicorn src.main:app --reload