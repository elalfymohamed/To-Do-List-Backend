from pydantic import BaseModel,ConfigDict,EmailStr,StringConstraints
from typing import Annotated


class LoginData(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8)]


    model_config = ConfigDict(from_attributes=True)






class Token(BaseModel):
    token: str
    user_id: str


