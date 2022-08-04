from pydantic import BaseModel
from typing import List
from .task_schemas import TaskBaseSchema

# Schema for the User Authentication
class UserAuthSchema(BaseModel):
    user_id: str
    username: str

    class Config:
        orm_mode = True

# Schema for the User
class UserSchema(UserAuthSchema):
    user_id: str
    username: str
    tasks: List[TaskBaseSchema] = []
    total_tasks: int
    finished_tasks: int
    unfinished_tasks: int

    class Config:
        orm_mode = True

# Schema for the User Login
class LoginSchema(BaseModel):
    username: str
    password: str

# Schema for the User Signup
class SignupSchema(LoginSchema):
    first_name: str
    last_name: str
    email: str
