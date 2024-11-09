def todo_item (item) -> dict:
  return {
        "id": str(item["_id"]),
        "title": item["title"],
        "completed": item["completed"],
        "description": item["description"],
        "created_at": item["created_at"],
        "updated_at": item["updated_at"],
        "deleted_at": item["deleted_at"]
    }




def todos_list(todos) -> list:
    return [todo_item(item) for item in todos]