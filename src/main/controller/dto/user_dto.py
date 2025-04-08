from pydantic import BaseModel, Field
from typing import Optional


class UserDTO(BaseModel):
    id: Optional[int] = Field(None, description="Unique identifier for the user")  # Used for updates
    username: str
    name: str
    email: str
    hashed_password: Optional[str] = None

class NewUserDTO(BaseModel):
    username: str
    name: str
    email: str
    password: str

class UserLoginDTO(BaseModel):
    username: str
    password: str