from pydantic import BaseModel
import datetime

# Schema for the Task Lis
class TaskBaseSchema(BaseModel):
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

# Schema for the Task Form
class TaskFormSchema(BaseModel):
    title: str
    description: str
    is_completed: bool = False
