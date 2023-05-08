from typing import List, Optional
import pydantic


class Address(pydantic.BaseModel):
    id: Optional[int]
    email_address: str

    class Config:
        orm_mode = True


class UserCreate(pydantic.BaseModel):
    name: str
    fullname: str
    addresses: Optional[List[Address]]


class User(pydantic.BaseModel):
    id: int
    name: str
    fullname: str
    addresses: List[Address]

    class Config:
        orm_mode = True
