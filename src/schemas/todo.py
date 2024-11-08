def todo(item) -> dict:
    return {
        "id": str(item["_id"]),
        "title": item["title"],
        "completed": item["completed"],
        "user_id": str(item["user_id"]),
        "description": item["description"],
        "created_at": item["created_at"],
        "updated_at": item["updated_at"]
    }




def todos_list(todos) -> list:
    return [todo(item) for item in todos]