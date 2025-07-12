from typing import List, Any
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from src.services.base import BaseDataManager, BaseService
from src.models.cuisines import CuisineModel
from src.schemas.cuisines import CuisineSchema, CuisineGetSchema
from src.schemas.cuisines import CuisineSuccessResponse
from src.schemas.responses import ErrorResponse, Status, ErrorMsg

class CuisineService(BaseService):
    
    async def get_cuisine_by_id(self, id: int) -> CuisineGetSchema | None:
        model = await CuisineDataManager(self.session).get_cuisine_by_prop(id, 'id')
         
        if model:
            return CuisineSuccessResponse(status=Status.SUCCESS, result=CuisineGetSchema.model_validate(model, from_attributes=True))
        else:
            return ErrorResponse(status=Status.ERROR, message=ErrorMsg.BAD_ID)  

class CuisineDataManager(BaseDataManager):

    async def get_cuisine_by_prop(self, val: Any, prop: str) -> List[CuisineModel] | None:
        query = select(CuisineModel).options(selectinload(CuisineModel.recipes)).where(getattr(CuisineModel, prop) == val)
        model = await self.get_one(query)
        return model

    async def add_cuisine(self, cuisine: CuisineSchema) -> CuisineModel | None:
        new_cuisine = CuisineModel(**cuisine.model_dump())
        await self.add_one(new_cuisine)
        return new_cuisine
    
    async def get_or_add_cuisine_by_name(self, name: str) -> CuisineModel | None:
        cuisine = await self.get_cuisine_by_prop(name, "name")
        if not cuisine:
            cuisine = await self.add_cuisine(CuisineSchema(name=name))
        return cuisine