from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    username: str
    email: str
