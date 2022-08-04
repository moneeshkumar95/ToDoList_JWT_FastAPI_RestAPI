from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


async def user_check(db: Session) -> None:
    """
    For checking the username and email already exist

    :param db: Session
    :return: None
    """
    try:
        db.commit()
    except IntegrityError as e:

        if 'user.username' in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Username already taken')
        elif 'user.email' in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Email already exist')