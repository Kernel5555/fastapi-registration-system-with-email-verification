from pydantic import BaseModel 
from datetime import datetime

class UserBase(BaseModel):
    username : str   
    email: str  
    password : str 
    is_active : bool = True
    first_name : str | None 
    last_name : str  | None
    sex : str | None
    is_superuser : bool = False 
    is_staff : bool = False
    ip_addr : str  
    email_code : str 
    activation_time_expires : datetime


class UserCreate(BaseModel):
    email: str   
    password : str 
    re_password: str


class UserResult(UserBase):
    id: str 

    class Config:
        orm_mode = True



"""
User Activation
"""
class UserActivationCreate(BaseModel):
    email: str
    activation_code : str  