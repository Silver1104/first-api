from pydantic import BaseModel, conint
from datetime import datetime
from typing import Annotated, Optional

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
        
class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: "UserOut" 
    model_config = {
        "from_attributes": True
    }

class PostVoteOut(BaseModel):
    Post: PostOut
    votes: int

    model_config = {
        "from_attributes": True
    }


class VoteBase(BaseModel):
    post_id: int
    user_id: int

from pydantic import Field

class VoteCreate(BaseModel):
    post_id: int
    vote_dir: Annotated[int, conint(ge=0, le=1)]

