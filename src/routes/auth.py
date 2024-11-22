from fastapi import Depends,APIRouter,status, Response
from db.mongodb import get_db
from models.auth import Token, LoginData,ForgatPassword,NewPassword
from models.user import User
from services.auth_service import Signup,Login,forgat_password,new_password



auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@auth_router.post("/signup", response_model=Token, tags=["auth"], summary="Create new user", description="Create new user", response_description="Create user success", status_code=status.HTTP_201_CREATED)
async def create_user( response: Response, user: User, db=Depends(get_db)):
    return await Signup(user,db,response)


@auth_router.post("/login", response_model=Token, tags=["auth"], summary="Login user", description="Login user", response_description="Login user success", status_code=status.HTTP_200_OK)
async def login_user( response: Response, login: LoginData, db=Depends(get_db)):
    return await Login(login,db,response)


@auth_router.post("/forgat-password", response_model=dict, tags=["auth"], summary="Forgat password", description="Forgat password", response_description="Forgat password success", status_code=status.HTTP_200_OK)
async def forgat_password_api(data: ForgatPassword, db=Depends(get_db)):
    return await forgat_password(data,db)

@auth_router.patch("/new-password", response_model=dict, tags=["auth"], summary="New password", description="New password", response_description="New password success", status_code=status.HTTP_200_OK)
async def new_password_api(data: NewPassword, db=Depends(get_db)):
    return await new_password(data,db)