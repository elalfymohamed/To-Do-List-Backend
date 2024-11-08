from fastapi import HTTPException,status
from datetime import datetime,timezone,timedelta
from models.user import User
from models.auth import LoginData, Token
from utils.auth_handler import create_access_token
from utils.pwd import get_password_hash,verify_password 

async def Signup(user: User,db: dict, response: dict = None) -> Token:
    
    user_dict = user.model_dump()

    is_user_exist = await db["users"].find_one({"email": user_dict["email"]})
        
    if is_user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exist")
        
    user_dict["password"] = get_password_hash(user_dict["password"])

    username = f'{user_dict["first_name"]} {user_dict["last_name"]}'

    user_dict.update({"created_at": datetime.now(), "updated_at": datetime.now(), "username": username})
        
    new_user = await db["users"].insert_one(user_dict)

    token_data = {
            "username": username,
            "user_id": str(new_user.inserted_id),
            "email": user_dict["email"],
    }
        
    token_access = create_access_token(token_data)

    response.set_cookie(key="access_token", value=token_access, httponly=True, samesite="none", secure=True, expires= datetime.now(timezone.utc) + timedelta(days=30))
        
    return {"user_id": str(new_user.inserted_id), "token": token_access}
    
  


    
async def Login(login: LoginData,db: dict, response: dict = None) -> Token:

    message_error = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Email or Password is incorrect"})

    user_dict = login.model_dump()


    is_user_exist = await db["users"].find_one({"email": user_dict["email"]})

    if not is_user_exist:
        raise message_error

    is_pass  = verify_password(user_dict["password"], is_user_exist["password"])

    if not is_pass:
        raise message_error
        

    token_data = {
            "username": is_user_exist["username"],
            "user_id": str(is_user_exist["_id"]),
            "email": is_user_exist["email"],
    }

    token_access = create_access_token(token_data)

    response.set_cookie(key="access_token", value=token_access, httponly=True, samesite="none", secure=True, expires= datetime.now(timezone.utc) + timedelta(days=30))

    return {"user_id": str(is_user_exist["_id"]), "token": token_access}
    