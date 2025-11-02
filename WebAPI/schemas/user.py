from pydantic import BaseModel, Field

class UserBase(BaseModel):
    email: str = Field(title="User's email", max_length=100)

class UserUpdateCode(UserBase):
    code: str = Field(title="Code for authentication", max_length=20)