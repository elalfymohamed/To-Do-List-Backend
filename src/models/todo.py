from fastapi import Header
from typing import Annotated

from pydantic import BaseModel,ConfigDict, StringConstraints
from datetime import datetime

class CreateTodo(BaseModel):
    title: Annotated[str, StringConstraints(min_length=2)]
    completed: bool = False
    description: Annotated[str, StringConstraints(min_length=10)]

    model_config = ConfigDict(from_attributes=True)



class ResponseTodo(BaseModel):
    id: str
    title: str
    completed: bool
    description: str
    created_at: datetime
    updated_at: datetime



class CommonHeaders(BaseModel):
    authorization: Annotated[str, Header()]

    