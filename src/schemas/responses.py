from pydantic import BaseModel
from enum import Enum

class Status(Enum):
    SUCCESS = 'success'
    ERROR = 'error'

class ErrorMsg(Enum):
    BAD_ID = 'Wrong id'
    DB_ERROR = 'Smth wrong with database'

class BaseResponse(BaseModel):
    status: Status

class ErrorResponse(BaseResponse):
    message: ErrorMsg
