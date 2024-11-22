from fastapi import APIRouter,Depends,status,Header
from models.todo import CreateTodo,CommonHeaders,ResponseTodo,ResponseTodos,ResponseDeleteTodo,UpdateTodo,DeleteTodo
from services.todo_service import create_todo,get_todos,soft_delete_todo,get_todo_by_id,update_todo,delete_todo,recently_deleted_todos,restore_recently_deleted_todo
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


@todo_router.get("/all", tags=["todos"], response_model=ResponseTodos,dependencies=[Depends(ValidateAccessToken)], description="Get todos", response_description="Get todos", status_code=status.HTTP_200_OK)
async def get_todos_api(headers: Annotated[CommonHeaders, Header()],db=Depends(get_db),limit:int | None = None):
    return await get_todos(limit,db,headers)


@todo_router.get("/get/{id}", tags=["todos"], response_model=ResponseTodo,  description="Get todo by id", response_description="Get todo by id", status_code=status.HTTP_200_OK)
async def get_todo_by_id_api(id: str, headers: Annotated[CommonHeaders, Header()],db=Depends(get_db)):
    return await get_todo_by_id(id, db,headers)


@todo_router.delete("/soft-delete/{id}", response_model=ResponseDeleteTodo, tags=["todos"], description="Soft Delete todo", response_description="Soft Delete todo", status_code=status.HTTP_200_OK)
async def soft_delete_todo_api(id: str, headers: Annotated[CommonHeaders, Header()],db=Depends(get_db)):
    return await soft_delete_todo(id,db,headers)


@todo_router.put("/update/{id}", response_model=ResponseTodo, tags=["todos"], description="Update todo", response_description="Update todo", status_code=status.HTTP_200_OK)
async def update_todo_api(id: str, todo: UpdateTodo, headers: Annotated[CommonHeaders, Header()],db=Depends(get_db)):
    return await update_todo(id,todo,db,headers)


@todo_router.delete("/delete", response_model=ResponseDeleteTodo, tags=["todos"], description="Delete todo", response_description="Delete todo", status_code=status.HTTP_200_OK)
async def delete_todo_api(todo: DeleteTodo, headers: Annotated[CommonHeaders, Header()],db=Depends(get_db)):
    return await delete_todo(todo,db,headers)


@todo_router.get("/recently-deleted", response_model=ResponseTodos, tags=["todos"], description="Get recently deleted todos", response_description="Get recently deleted todos", status_code=status.HTTP_200_OK)
async def recently_deleted_todos_api(headers: Annotated[CommonHeaders, Header()],db=Depends(get_db),limit:int | None = None):
    return await recently_deleted_todos(limit,db,headers)

@todo_router.patch("/recently-deleted", response_model=ResponseDeleteTodo, tags=["todos"], description="Restore recently deleted todo", response_description="Restore recently deleted todo", status_code=status.HTTP_200_OK)
async def restore_recently_deleted_todo_api(todo: DeleteTodo, headers: Annotated[CommonHeaders, Header()],db=Depends(get_db)):
    return await restore_recently_deleted_todo(todo,db,headers)