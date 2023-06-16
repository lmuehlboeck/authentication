from pydantic import BaseModel

class User(BaseModel):
    id: int = 0
    username: str
    role: int = 0

class UserLogin(BaseModel):
    username: str
    password: str
    role: int = 0

