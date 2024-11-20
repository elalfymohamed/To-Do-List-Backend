from fastapi import APIRouter,Depends,status,Header
from models.todo import CommonHeaders
from db.mongodb import get_db
from typing import Annotated
from models.user import ResponseUser
from middleware.validate_access_token import ValidateAccessToken
from services.user_service import get_user



user_router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    responses={404: {"description": "Not found"}},
)



@user_router.get("/", response_model=ResponseUser, tags=["profile"], dependencies=[Depends(ValidateAccessToken)], description="Get user details", response_description="Get user details", status_code=status.HTTP_200_OK)
async def get_user_api(headers: Annotated[CommonHeaders, Header()],db=Depends(get_db)):
    return await get_user(db,headers)