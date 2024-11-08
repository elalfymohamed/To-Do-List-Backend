from fastapi import HTTPException,status
from models.todo import CreateTodo,ResponseTodo
from utils.decode_token import decode_token
from datetime import datetime
from schemas.todo import todo_item

async def create_todo(todo: CreateTodo, db: dict, headers: dict) -> ResponseTodo:

    todo_dict = todo.model_dump()

    user_data = decode_token(headers)

    is_user_exist = await db["users"].find_one({"email": user_data["email"]})

    if not is_user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    

    todo_dict["created_at"] = datetime.now()
    todo_dict["updated_at"] = datetime.now()
    todo_dict["user_id"] = str(is_user_exist["_id"])

    new_todo = await db["todos"].insert_one(todo_dict)

    if not new_todo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Todo not created")
    
    return todo_item({**todo_dict, "_id": str(new_todo.inserted_id)})


    

