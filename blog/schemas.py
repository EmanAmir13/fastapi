from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class Show(BaseModel):
    title: str
    body: str

    class Config():
        orm_mode = True


class User(BaseModel):
    email: str
    username: str
    password: str


class ShowUser(BaseModel):
    email: str
    username: str

    class Config():
        orm_mode = True
