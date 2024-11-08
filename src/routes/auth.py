from fastapi import Depends,APIRouter,status, Response
from db.mongodb import get_db
from models.auth import Token, LoginData
from models.user import User
from services.auth_service import Signup,Login



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