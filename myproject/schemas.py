from typing import List
import datetime as _dt
import pydantic as _pydantic

class _PostBase(_pydantic.BaseModel):
    currentclub: str
    age: int
    position: str



class PostCreate(_PostBase):
    position: str

class Post(_PostBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True

class _PlayerBase(_pydantic.BaseModel):
    playernumber: int
    firstname: str
    lastname: str


class PlayerCreate(_PlayerBase):
    firstname: str
    lastname: str





class Player(_PlayerBase):
    id: int
    is_active = bool
    posts: List[Post] = []

    class Config:
        orm_mode = True