from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.base import Task
from schemas.user_schemas import UserSchema


async def check_task(_id: str, db: Session, user_id: int) -> Task:
    """
    For checking the task is present in the db & it belong the current user

    :param _id: Task ID
    :param db: Session
    :param user_id: User ID
    :return: Task data
    """
    raw_task = db.query(Task).filter(Task.task_id == _id)
    task = raw_task.first()
    not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail='Task not found')
    if (not task) or (task.user_id != user_id):
        raise not_found_exception
    return raw_task


async def task_count(user: UserSchema) -> UserSchema:
    """
    For counting the current user Total Task, Finished Task & Unfinished Task

    :param user: Task ID
    :return: Task data + Total Task, Finished Task & Unfinished Task data
    """
    tasks = user.tasks
    total_tasks = len(tasks)
    finished_tasks = sum(map(lambda x: 1 if x.is_completed else 0, tasks))
    unfinished_tasks = total_tasks - finished_tasks
    user.total_tasks = total_tasks
    user.finished_tasks = finished_tasks
    user.unfinished_tasks = unfinished_tasks
    return user
