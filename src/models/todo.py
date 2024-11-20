from fastapi import Header
from typing import Annotated,Union

from pydantic import BaseModel,ConfigDict, StringConstraints
from datetime import datetime

class CreateTodo(BaseModel):
    title: Annotated[str, StringConstraints(min_length=2)]
    completed: bool = False
    description: Annotated[str, StringConstraints(min_length=10)]
    deleted_at: None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateTodo(BaseModel):
    title: Annotated[str, StringConstraints(min_length=2)]
    completed: bool = False
    description: Annotated[str, StringConstraints(min_length=10)]

    model_config = ConfigDict(from_attributes=True)



class DeleteTodo(BaseModel):
    deleted_at: datetime
    id: str


class ResponseTodo(BaseModel):
    id: str
    title: str
    completed: bool
    description: str
    created_at: datetime
    updated_at: datetime
    deleted_at: None = None | datetime


class ResponseDeleteTodo(BaseModel):
    id: str
    detail: str


class ResponseTodos(BaseModel):
    todos: Union[list[ResponseTodo], list]

class CommonHeaders(BaseModel):
    authorization: Annotated[str, Header()]

    