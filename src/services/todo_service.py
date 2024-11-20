from fastapi import HTTPException,status
from models.todo import CreateTodo,ResponseTodo,ResponseTodos,ResponseDeleteTodo,UpdateTodo,DeleteTodo
from utils.decode_token import decode_token
from datetime import datetime
from schemas.todo import todo_item,todos_list

from bson.objectid import ObjectId



# create todo service
async def create_todo(todo: CreateTodo, db: dict, headers: dict) -> ResponseTodo:
    """
    Create a new todo

    Args:
    - todo (CreateTodo): new todo
    - db (dict): database connection
    - headers (dict): request headers

    Returns:
    - ResponseTodo: new todo

    Raises:
    - HTTPException(404): if the user do not exist
    - HTTPException(400): if the todo is not created
    """
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
    """
    Get all todos for a user

    Args:
    - limit (int): limit of the response
    - db (dict): database connection
    - headers (dict): request headers

    Returns:
    - ResponseTodos: todos for the user

    Raises:
    - HTTPException(404): if the user do not exist
    """
    user_data = decode_token(headers)

    is_user_exist = await db["users"].find_one({"email": user_data["email"]})

    if not is_user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    todos = await db["todos"].find({"user_id": str(is_user_exist["_id"]), "deleted_at": None}).sort("created_at", -1).to_list(limit)

    return {"todos": todos_list(todos)}

# get todo by id service

async def get_todo_by_id(id: str, db: dict, headers: dict) -> ResponseTodo:
    """
    Get a todo by id

    Args:
    - id (str): id of the todo to get
    - db (dict): database connection
    - headers (dict): request headers

    Returns:
    - ResponseTodo: the todo requested

    Raises:
    - HTTPException(400): if the Todo ID is invalid
    - HTTPException(404): if the user or todo do not exist
    """
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
    """
    Soft delete a todo item by marking it as deleted.

    Args:
    - id (str): The ID of the todo to be soft deleted.
    - db (dict): Database connection.
    - headers (dict): Request headers containing authorization.

    Returns:
    - ResponseDeleteTodo: A response containing the ID and detail of the soft-deleted todo.

    Raises:
    - HTTPException(404): If the user or todo do not exist.
    - HTTPException(400): If the todo is already deleted or if the ID is invalid.
    - HTTPException(500): If the soft delete operation fails.
    """
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
    
    if todo["deleted_at"] is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Todo already deleted")

    result =  await db["todos"].update_one({"_id": todo_id}, {"$set": {"deleted_at": datetime.now()}}) 
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete todo")

    return {"id": str(todo_id), "detail": "Todo soft deleted"}




# update todo service

async def update_todo(id: str, todo: UpdateTodo, db: dict, headers: dict) -> ResponseTodo:
    """
    Update a todo item.

    Args:
    - id (str): The ID of the todo to be updated.
    - todo (UpdateTodo): The updated todo item.
    - db (dict): Database connection.
    - headers (dict): Request headers containing authorization.

    Returns:
    - ResponseTodo: A response containing the ID and detail of the updated todo.

    Raises:
    - HTTPException(404): If the user or todo do not exist.
    - HTTPException(400): If the ID is invalid.
    - HTTPException(500): If the update operation fails.
    """
    user_data = decode_token(headers)

    is_user_exist = await db["users"].find_one({"email": user_data["email"]})

    if not is_user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    try:
        todo_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Todo ID format")
    
    todo_dict = todo.model_dump()

    todo_dict["updated_at"] = datetime.now()

    todo = await db["todos"].find_one({"_id": todo_id, "user_id": str(is_user_exist["_id"]), "deleted_at": None})

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    result = await db["todos"].update_one({"_id": todo_id}, {"$set": todo_dict})

    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update todo")

    return todo_item({**todo_dict, "_id": str(todo_id)})




# delete todo service

async def delete_todo(todo: DeleteTodo, db: dict, headers: dict) -> ResponseDeleteTodo:
    """
    Delete a todo item by ID.

    Args:
    - todo (DeleteTodo): id and deleted_at of the todo to delete
    - db (dict): database connection
    - headers (dict): request headers

    Returns:
    - ResponseDeleteTodo: id and detail of the deleted todo

    Raises:
    - HTTPException(404): If the user or todo do not exist.
    - HTTPException(400): If the todo is not deleted or if the ID is invalid.
    - HTTPException(500): If the delete operation fails.
    """
    user_data = decode_token(headers)

    is_user_exist = await db["users"].find_one({"email": user_data["email"]})

    if not is_user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    todo_delete = todo.model_dump() 
    
    try:
        todo_id = ObjectId(todo_delete['id'])
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Todo ID format")
    
    todo = await db["todos"].find_one({"_id": todo_id, "user_id": str(is_user_exist["_id"]), "deleted_at": todo_delete["deleted_at"]})
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    result = await db["todos"].delete_one({"_id": todo_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete todo")

    return {"id": str(todo_id), "detail": "Todo deleted"}

    
# return todo service

async def restore_recently_deleted_todo(todo: DeleteTodo,db: dict, headers: dict) -> ResponseDeleteTodo:
    """
    Restore a deleted todo

    Args:
    - todo (DeleteTodo): id and deleted_at of the todo to restore
    - db (dict): database connection
    - headers (dict): request headers

    Returns:
    - ResponseDeleteTodo: _id and detail of the restored todo

    Raises:
    - HTTPException(404): if the user or todo do not exist
    - HTTPException(400): if the todo is not deleted or if the id is invalid
    - HTTPException(500): if the restore operation fails
    """
    
    user_data = decode_token(headers)

    is_user_exist = await db["users"].find_one({"email": user_data["email"]})

    if not is_user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    todo_delete = todo.model_dump() 
    
    try:
        todo_id = ObjectId(todo_delete['id'])
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Todo ID format")
    

    todo = await db["todos"].find_one({"_id":todo_id, "user_id": str(is_user_exist["_id"]), "deleted_at": todo_delete["deleted_at"]})

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    if todo["deleted_at"] is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Todo not deleted")
    
    result = await db["todos"].update_one({"_id": todo_id}, {"$set": {"deleted_at": None}})
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to restore todo")
    
    return {"id": str(todo_id), "detail": "Todo restored"}
    





async def recently_deleted_todos(limit,db: dict, headers: dict) -> ResponseTodos:
    """
    Get recently deleted todos

    Args:
    - limit (int): limit of the response
    - db (dict): database connection
    - headers (dict): request headers

    Returns:
    - ResponseTodos: recently deleted todos

    Raises:
    - HTTPException(404): if the user do not exist
    - HTTPException(404): if no todos are found
    """
    user_data = decode_token(headers)

    is_user_exist = await db["users"].find_one({"email": user_data["email"]})

    if not is_user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    todos = await db["todos"].find({"user_id": str(is_user_exist["_id"]), "deleted_at": {"$ne": None}}).sort("created_at", -1).to_list(limit)

    if not todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No todos found")

    return {"todos": todos_list(todos)}
