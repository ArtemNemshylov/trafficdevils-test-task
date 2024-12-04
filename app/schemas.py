from pydantic import BaseModel


class RequestBase(BaseModel):
    bottoken: str
    chatid: str
    message: str


class RequestCreate(RequestBase):
    pass


class RequestOut(RequestBase):
    id: int
    user_id: int
    response: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    role: str


class UserCreate(BaseModel):
    username: str
    password: str
    role: str

    class Config:
        from_attributes = True


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True
