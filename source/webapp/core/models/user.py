from webapp.core.models.generic import GenericBase


class UserBase(GenericBase):
    username: str
    email: str


class UserCreate(UserBase):
    pass
