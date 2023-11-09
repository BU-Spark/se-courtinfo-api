from pydantic import BaseModel, UUID4
import typing as t


class UserBase(BaseModel):
    email: str
    is_active: bool = False
    is_superuser: bool = False
    is_county_authorized: bool = False
    first_name: str = None
    last_name: str = None


class UserOut(UserBase):
    id: UUID4


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: UUID4

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"
