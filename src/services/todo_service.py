from fastapi import HTTPException,status
from models.todo import CreateTodo,CommonHeaders
from utils.auth_handler import decode_jwt







async def create_todo(todo: CreateTodo, db: dict, headers: CommonHeaders) -> CreateTodo:

    todo_dict = todo.model_dump()

    token = headers.Authorization

    decoded_token = decode_jwt(token)

    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Not authenticated'
        )

    print(decoded_token)
#     user_id = decoded_token.get("user_id")

#    is_user_exists = db["users"].find_one({"_id": str(user_id)})

