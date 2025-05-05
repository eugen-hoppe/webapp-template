from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    username: str
    email: str
