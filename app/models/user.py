from pydantic import BaseModel


class UserBaseModel(BaseModel):
    name: str
    lastname: str


class UserCreateModel(UserBaseModel):
    password: str


class UserLoginModel(BaseModel):
    username: str
    password: str


class UserResponseModel(UserBaseModel):
    username: str
