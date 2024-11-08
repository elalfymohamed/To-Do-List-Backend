
from typing import Annotated

from pydantic import BaseModel,ConfigDict, EmailStr, StringConstraints,field_validator


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

