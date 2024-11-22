from fastapi import HTTPException,status
from datetime import datetime,timezone,timedelta
from models.user import User
from models.auth import LoginData, Token,ForgatPassword,NewPassword
from utils.auth_handler import create_access_token,create_reset_token,decode_jwt
from utils.pwd import get_password_hash,verify_password 
from utils.send_email import send_email



async def Signup(user: User,db: dict, response: dict = None) -> Token:
    
    """
    Create a new user

    Args:
    - user (User): new user
    - db (dict): database connection
    - response (dict, optional): response object to set the cookie. Defaults to None.

    Raises:
    - HTTPException(400): if the user already exist

    Returns:
    - Token: a token access with the user id and email
    """
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

    """
    Login a user and return a token access.

    Args:
    - login (LoginData): login data of the user.
    - db (dict): database connection.
    - response (dict, optional): response object to set the cookie. Defaults to None.

    Raises:
    - HTTPException(404): if the user do not exist or email or password is incorrect.

    Returns:
    - Token: a token access with the user id and email.
    """
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
    




async def forgat_password(data: ForgatPassword,db: dict) -> dict:
    
    """
    Sends a password reset email to the user if they exist.

    Args:
    - data (ForgatPassword): Contains the user's email.
    - db (dict): The database connection.

    Returns:
    - dict: A message indicating that the email was sent successfully.

    Raises:
    - HTTPException(400): If the user does not exist.
    - HTTPException(500): If there is an error sending the email.
    """
    email = data.model_dump()["email"]
    
    is_user_exist = await db["users"].find_one({"email": email})
        
    if is_user_exist is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    token_data = {
            "email": email,
            "expire": int(expire.timestamp())
    }

    token = create_reset_token(token_data)
    
    await db["users"].update_one({"email": email}, {"$set": {"reset_token": token}})

    subject = "Reset Password"

    message = f"""
    <html>
    <body>
    <p>Hi {is_user_exist["username"]},</p>
    <p>Click on the link below to reset your password:</p>
    <a href="http://localhost:8000/reset-password?token={token}">Reset Password</a> 
    </body>
    </html>
    """

    try:
        await send_email(email, subject, message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"message": "Email sent successfully"}


    

async def new_password(data: NewPassword,db: dict) -> dict:
      
    """
    Update the user's password using a reset token.

    Args:
    - data (NewPassword): An object containing the new password and reset token.
    - db (dict): The database connection.

    Returns:
    - dict: A message indicating the password was updated successfully.

    Raises:
    - HTTPException(400): If the token is invalid or expired.
    - HTTPException(400): If the user does not exist or the password update fails.
    """
    user_data = data.model_dump()


    decode_token = decode_jwt(user_data["reset_token"])

    if not decode_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")


    is_user_exist = await db["users"].find_one({"email": decode_token["email"]})

    if is_user_exist["reset_token"] != user_data["reset_token"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

    if datetime.now(timezone.utc) > datetime.fromtimestamp(decode_token["expire"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")

    if is_user_exist is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    
    new_password = get_password_hash(user_data["password"])

    result = await db["users"].update_one({"email": decode_token["email"]}, {"$set": {"password": new_password}})

    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update password")

    return {"message": "Password updated successfully"}


    

    
    