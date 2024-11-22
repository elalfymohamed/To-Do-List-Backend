
from typing import Annotated

from pydantic import BaseModel,ConfigDict, EmailStr, StringConstraints,field_validator

from datetime import datetime

class User(BaseModel):
    last_name: Annotated[str, StringConstraints(min_length=2)]
    first_name: Annotated[str, StringConstraints(min_length=2)]
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8), ]

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

    model_config = ConfigDict(from_attributes=True)



class ResponseUser(BaseModel):
    email: EmailStr
    username: str
    id: str
    last_name: str
    first_name: str
    created_at: datetime
    updated_at: datetime
    



class ResatPassword(BaseModel):
    current_password: Annotated[str, StringConstraints(min_length=8)]
    new_password: Annotated[str, StringConstraints(min_length=8)]
    confirm_password: Annotated[str, StringConstraints(min_length=8)]

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if v != cls.confirm_password:
            raise ValueError("Password and confirm password do not match")
        return v
    
    model_config = ConfigDict(from_attributes=True)
  




class UpdateUser(BaseModel):
    last_name: Annotated[str, StringConstraints(min_length=2)]
    first_name: Annotated[str, StringConstraints(min_length=2)]
    email: EmailStr
   
    model_config = ConfigDict(from_attributes=True)