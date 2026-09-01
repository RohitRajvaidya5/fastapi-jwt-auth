
from pydantic import BaseModel

class UserCreate(BaseModel):
    username : str
    email : str
    password : str

class UserResponse(BaseModel):
    id : int
    username : str
    email : str
    role : str

    model_config = {
        "from_attributes":True
    }

class UserUpdate(BaseModel):
    username : str
    email : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str
