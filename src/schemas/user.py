def user(item) -> dict:
    return {
        "id": str(item["_id"]),
        "last_name": item["last_name"],
        "first_name": item["first_name"],
        "email": item["email"],
        "password": item["password"],
        "created_at": item["created_at"],
        "updated_at": item["updated_at"]
    }




def users_list(items) -> list:
    return [user(item) for item in items]


