from fastapi import Header
from typing import Annotated

from pydantic import BaseModel,ConfigDict, StringConstraints

class CreateTodo(BaseModel):
    title: Annotated[str, StringConstraints(min_length=2)]
    completed: bool = False
    description: Annotated[str, StringConstraints(min_length=10)]

    model_config = ConfigDict(from_attributes=True)





class CommonHeaders(BaseModel):
    Authorization: Annotated[str, Header()]
    x_length: int = 100
    