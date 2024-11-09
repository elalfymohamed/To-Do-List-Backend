from fastapi import HTTPException,status
from models.todo import CreateTodo,ResponseTodo,ResponseTodos,ResponseDeleteTodo
from utils.decode_token import decode_token
from datetime import datetime
from schemas.todo import todo_item,todos_list

from bson.objectid import ObjectId



# create todo service
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


    
#  get todos service

async def get_todos(limit,db: dict, headers: dict) -> ResponseTodos:
    user_data = decode_token(headers)

    is_user_exist = await db["users"].find_one({"email": user_data["email"]})

    if not is_user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    todos = await db["todos"].find({"user_id": str(is_user_exist["_id"]), "deleted_at": None}).sort("created_at", -1).to_list(limit)

    return {"todos": todos_list(todos)}

# get todo by id service

async def get_todo_by_id(id: str, db: dict, headers: dict) -> ResponseTodo:
    user_data = decode_token(headers)

    is_user_exist = await db["users"].find_one({"email": user_data["email"]})

    if not is_user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    try:
        todo_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Todo ID format")
    
    todo = await db["todos"].find_one({"_id": todo_id, "user_id": str(is_user_exist["_id"]), "deleted_at": None})

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    return todo_item(todo)
    
# soft delete todo service

async def soft_delete_todo(id: str, db: dict, headers: dict) -> ResponseDeleteTodo:
    user_data = decode_token(headers)

    is_user_exist = await db["users"].find_one({"email": user_data["email"]})

    if not is_user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    try:
        todo_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Todo ID format")
    
    todo = await db["todos"].find_one({"_id": todo_id, "user_id": str(is_user_exist["_id"]), "deleted_at": None})

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    result =  await db["todos"].update_one({"_id": todo_id}, {"$set": {"deleted_at": datetime.now()}}) 
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete todo")

    return {"id": str(todo_id)}


