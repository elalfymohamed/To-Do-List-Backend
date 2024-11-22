from pydantic import BaseModel,ConfigDict, EmailStr, StringConstraints,field_validator

from typing import Annotated,List


class LoginData(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8)]


    model_config = ConfigDict(from_attributes=True)



class EmailSchema(BaseModel):
    email: List[EmailStr]

class ForgatPassword(BaseModel):
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)



class NewPassword(BaseModel):
    new_password: Annotated[str, StringConstraints(min_length=8)]
    confirm_password: Annotated[str, StringConstraints(min_length=8)]
    reset_token: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v:str):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if v != cls.confirm_password:
            raise ValueError("Password and confirm password do not match")
        return v

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    token: str
    user_id: str


