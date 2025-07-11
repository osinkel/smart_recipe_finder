from fastapi import FastAPI
from src.routers import main_router
import uvicorn


app = FastAPI(
    title='Smart recipe finder',
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0") # uvicorn src.main:app --reload