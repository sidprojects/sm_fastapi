from  datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class CreatePost(PostBase):
    pass

class UserOutput(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOutput
    
    class Config:
        orm_mode = True

        
class PostOut(BaseModel):
    Post: Post
    num_votes: int   
    
    class Config:
        orm_mode = True  
        
class CreateUser(BaseModel):
    email: EmailStr
    password: str
    

        
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] =  None
    
class Vote(BaseModel):
    post_id: int
    up_vote: bool = True