from fastapi import APIRouter,Depends,status,Header
from models.todo import CreateTodo,CommonHeaders,ResponseTodo
from services.todo_service import create_todo
from db.mongodb import get_db
from middleware.validate_access_token import ValidateAccessToken
from typing import Annotated

todo_router = APIRouter(
    prefix="/todo",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)



@todo_router.post("/create", tags=["todos"], response_model=ResponseTodo,dependencies=[Depends(ValidateAccessToken)], description="Create new todo", response_description="Created todo", status_code=status.HTTP_201_CREATED)
async def create_todo_api(headers: Annotated[CommonHeaders, Header()],todo: CreateTodo, db=Depends(get_db)):
    return await create_todo(todo, db,headers) 