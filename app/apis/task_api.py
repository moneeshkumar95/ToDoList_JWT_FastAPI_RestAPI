from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.base import User, get_db, Task
from schemas.user_schemas import UserSchema, UserAuthSchema
from schemas.task_schemas import TaskFormSchema, TaskSchema, TaskSearchSchema, TaskListSchema
from schemas.response_schema import SuccessSchema
from utils.jwt_manager import get_current_user
from utils.response import success_response
from utils.task_utils import check_task, task_count
import datetime

# Creating the APIRouter instance & setting prefix, tags
router = APIRouter(prefix='/api/task',
                   tags=['Task'])


@router.get('/', response_model=SuccessSchema)
async def home(user: UserSchema = Depends(get_current_user)):
    """
    API for the current user Task List

    :Authorization: access_token
    :return:  task list, total_task, finished_task, unfinished task, user_id, username
    """
    user = await task_count(user=user)
    return success_response(detail='Data retrieved successfully',
                            data=UserSchema.from_orm(user))


@router.get("/search", response_model=SuccessSchema)
async def task_search(title: str, user: UserAuthSchema = Depends(get_current_user), 
                      db: Session = Depends(get_db)):
    user.tasks = list(filter(lambda x: title in x.title, user.tasks))
    
    return success_response(detail='Task revertived succesfully',
                            data=TaskListSchema.from_orm(user))
    
    
@router.post('/', response_model=SuccessSchema)
async def create_task(request: TaskFormSchema, user: UserAuthSchema = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    """
    API to create a new task

    :JSON data: title, description, is_completed
    :Authorization: access_token
    :return: status_code, detail, Task data
    """
    data = request.dict()
    data['user_id'] = user.user_id
    task = Task(**data)
    db.add(task)
    db.commit()
    db.refresh(task)

    return success_response(status_code=status.HTTP_201_CREATED,
                            detail='Task created successfully',
                            data=TaskSchema.from_orm(task))


@router.get('/{_id}', response_model=SuccessSchema)
async def get_task(_id: str, user: UserAuthSchema = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    API to get the task data

    :_id: Task ID
    :Authorization: access_token
    :return: status_code, detail, Task data
    """
    task = await check_task(_id=_id, db=db, user_id=user.user_id)
    return success_response(detail='Task retrieved successfully',
                            data=TaskSchema.from_orm(task.first()))


@router.put('/{_id}', response_model=SuccessSchema)
async def update_task(_id: str, request: TaskFormSchema, user: UserAuthSchema = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    """
    API to update the task

    :_id: Task ID
    :JSON data: Task data
    :Authorization: access_token
    :return: status_code, detail, Task data
    """
    data = request.dict()
    data['updated_at'] = datetime.datetime.utcnow()
    task = await check_task(_id=_id, db=db, user_id=user.user_id)
    task.update(data)
    db.commit()

    return success_response(status_code=status.HTTP_202_ACCEPTED,
                            detail='Task updated successfully',
                            data=TaskSchema.from_orm(task.first()))


@router.delete('/{_id}')
async def delete_task(_id: str, user: UserAuthSchema = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    API to delete the task

    :_id: Task ID
    :Authorization: access_token
    :return: status_code, detail, Task data
    """
    task = await check_task(_id=_id, db=db, user_id=user.user_id)
    task.delete()
    db.commit()

    return success_response(status_code=status.HTTP_202_ACCEPTED,
                            detail='Task deleted successfully')


@router.put('/status_update/{_id}')
async def update_task_status(_id: str, user: UserAuthSchema = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    API to update the task status(is_completed)

    :_id: Task ID
    :Authorization: access_token
    :return: status_code, detail, Task data
    """
    raw_task = await check_task(_id=_id, db=db, user_id=user.user_id)
    task = raw_task.first()
    task.is_completed = not task.is_completed
    task.updated_at = datetime.datetime.utcnow()
    db.add(task)
    db.commit()

    return success_response(status_code=status.HTTP_202_ACCEPTED,
                            detail='Task updated successfully',
                            data=TaskSchema.from_orm(task))