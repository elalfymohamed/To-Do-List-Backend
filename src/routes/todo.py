from fastapi import APIRouter,Depends,status,Header
from models.todo import CreateTodo,CommonHeaders,ResponseTodo
from schemas.todo import todos_list
from services.todo_service import create_todo,get_todos
from db.mongodb import get_db
from middleware.validate_access_token import ValidateAccessToken
from typing import Annotated,Union

todo_router = APIRouter(
    prefix="/todo",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)



@todo_router.post("/create", tags=["todos"], response_model=ResponseTodo,dependencies=[Depends(ValidateAccessToken)], description="Create new todo", response_description="Created todo", status_code=status.HTTP_201_CREATED)
async def create_todo_api(headers: Annotated[CommonHeaders, Header()],todo: CreateTodo, db=Depends(get_db)):
    return await create_todo(todo, db,headers) 



@todo_router.get("/all", tags=["todos"], response_model=Union[list[ResponseTodo], list],dependencies=[Depends(ValidateAccessToken)], description="Get todos", response_description="Get todos", status_code=status.HTTP_200_OK)
async def get_todos_api(headers: Annotated[CommonHeaders, Header()],db=Depends(get_db),limit:int | None = None):
    return await get_todos(limit,db,headers)