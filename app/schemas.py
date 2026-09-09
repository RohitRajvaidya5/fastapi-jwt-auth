
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username : str
    email : str
    password : str
    role : str

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

class PostCreate(BaseModel):
    title : str = Field(min_length=1, max_length=100)
    content : str = Field(min_length=1)

class PostResponse(BaseModel):
    id : int
    title : str
    content : str
    owner_id : int

    model_config = {
        "from_attributes":True
    }
