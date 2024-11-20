from fastapi import HTTPException,status
from models.user import ResponseUser
from utils.decode_token import decode_token
from schemas.user import user_information

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


