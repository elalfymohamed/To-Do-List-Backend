from fastapi import HTTPException,status
from models.user import ResponseUser,ResatPassword,UpdateUser
from utils.decode_token import decode_token
from schemas.user import user_information
from utils.pwd import verify_password,get_password_hash
from datetime import datetime

from bson.objectid import ObjectId


async def get_user(db: dict, headers: dict) -> ResponseUser:
  """
  Get user details by email

  Args:
  - db (dict): Database connection.
  - headers (dict): Request headers containing authorization.

  Returns:
  - dict: User details.

  Raises:
  - HTTPException(404): If the user does not exist.
  """
  user_data = decode_token(headers)

  is_user_exist = await db["users"].find_one({"email": user_data["email"]})

  if not is_user_exist:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

  return user_information(is_user_exist)



async def reset_password(data: ResatPassword, db: dict,headers: dict) -> dict:
 
    """
    Reset the user's password.

    Args:
    - data (ResatPassword): An object containing the current password, new password, and token.
    - db (dict): The database connection.

    Returns:
    - dict: A message indicating the password was reset successfully.

    Raises:
    - HTTPException(404): If the user does not exist.
    - HTTPException(400): If the current password is incorrect.
    """
    user_data = decode_token(headers)

    is_user_exist = await db["users"].find_one({"email": user_data["email"]})

    if not is_user_exist:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    is_valid = verify_password(data.current_password,is_user_exist["password"])

    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    
    new_password = get_password_hash(data.new_password)

    await db["users"].update_one({"email": user_data["email"]}, {"$set": {"password": new_password}})

    return {"message": "Password reset successfully"}




async def update_profile(user: UpdateUser,db: dict,headers: dict) -> ResponseUser:
   
    """
    Update user details.

    Args:
    - user (UpdateUser): An object containing updated user details.
    - db (dict): Database connection.
    - headers (dict): Request headers containing authorization.

    Returns:
    - ResponseUser: Updated user details.

    Raises:
    - HTTPException(404): If the user does not exist.
    - HTTPException(400): If the email already exists.
    """
    user_data = decode_token(headers)

    is_user_exist = await db["users"].find_one({"email": user_data["email"]})

    if not is_user_exist:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    

    if user["email"]:
      is_user_exist = await db["users"].find_one({"email": user["email"]})

      if is_user_exist: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist")

    user_dict = user.model_dump()

    user_dict["updated_at"] = datetime.now()

    result =  await db["users"].update_one({"email": user_data["email"]}, {"$set": user_dict})

    if result.modified_count == 0:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    updated_user = await db["users"].find_one({"email": user_dict["email"]})

    return user_information(updated_user)

   

