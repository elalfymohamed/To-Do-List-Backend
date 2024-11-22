from fastapi import APIRouter,Depends,status,Header
from models.todo import CommonHeaders
from db.mongodb import get_db
from typing import Annotated
from models.user import ResponseUser,UpdateUser,ResatPassword
from middleware.validate_access_token import ValidateAccessToken
from services.user_service import get_user,update_profile,reset_password



user_router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    responses={404: {"description": "Not found"}},
)



@user_router.get("/", response_model=ResponseUser, tags=["profile"], dependencies=[Depends(ValidateAccessToken)], description="Get user details", response_description="Get user details", status_code=status.HTTP_200_OK)
async def get_user_api(headers: Annotated[CommonHeaders, Header()],db=Depends(get_db)):
    return await get_user(db,headers)


@user_router.patch("/reset-password", response_model=ResponseUser, tags=["profile"], dependencies=[Depends(ValidateAccessToken)], description="Reset password", response_description="Reset password", status_code=status.HTTP_200_OK)
async def reset_password_api(data: ResatPassword, headers: Annotated[CommonHeaders, Header()],db=Depends(get_db)):
    return await reset_password(data,db,headers)


@user_router.put("/update", response_model=ResponseUser, tags=["profile"], dependencies=[Depends(ValidateAccessToken)], description="Update profile", response_description="Update profile", status_code=status.HTTP_200_OK)
async def update_profile_api(user: UpdateUser, headers: Annotated[CommonHeaders, Header()],db=Depends(get_db)):
    return await update_profile(user,db,headers)