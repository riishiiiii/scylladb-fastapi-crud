from pydantic import BaseModel
from uuid import UUID


class User(BaseModel):
    name: str
    email: str
    age: int


class UserResponse(User):
    id: UUID
