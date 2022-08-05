from asyncio import tasks
from turtle import st, title
from typing import List
from pydantic import BaseModel
import datetime

# Schmea for the Task Search
class TaskSearchSchema(BaseModel):
    title: str


# Schema for the Task
class TaskBaseSchema(TaskSearchSchema):
    task_id: str
    title: str
    is_completed: bool

    class Config:
        orm_mode = True

# Schema for the Task detailed
class TaskSchema(TaskBaseSchema):
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
        
# Schema for the Task List
class TaskListSchema(BaseModel):
    tasks: List[TaskBaseSchema]

    class Config:
        orm_mode = True

# Schema for the Task Form
class TaskFormSchema(BaseModel):
    title: str
    description: str
    is_completed: bool = False
