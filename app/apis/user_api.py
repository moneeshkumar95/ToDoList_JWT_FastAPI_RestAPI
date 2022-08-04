from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.base import User, get_db, JwtBlocklist
from schemas.user_schemas import LoginSchema, SignupSchema
from utils.jwt_manager import auth_required, create_access_token
from utils.user_utils import user_check
import datetime

# Creating the APIRouter instance & setting prefix, tags
router = APIRouter(prefix='/api/user',
                   tags=['User'])


@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(request: SignupSchema, db: Session = Depends(get_db)):
    """
    API to create a new user

    :JSON data: first_name, last_name, username, email, password
    :return: detail, access_token, refresh_token, token_type
    """
    user = User(**request.dict())
    db.add(user)
    await user_check(db=db)
    db.refresh(user)
    token = {"detail": 'User created successfully',
             "access_token": create_access_token(data={'sub': user.user_id}),
             "token_type": "bearer"}

    return token


@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    API for user Login

    :JSON data: username,  password
    :return: detail, access_token, refresh_token, token_type
    """
    user = db.query(User).filter(User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')

    if not user.verify_password(request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid password')

    token = {"detail": 'User created successfully',
             "access_token": create_access_token(data={'sub': user.user_id}),
             "token_type": "bearer"}

    return token


@router.delete('/logout')
async def logout(Token_Data: dict = Depends(auth_required), db: Session = Depends(get_db)):
    """
    API for user logout

    :Authorization: access_token
    :return: detail
    """
    jti = Token_Data.get('jti')
    ttl = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    jwtblocklist = JwtBlocklist(jti=jti, ttl=ttl)
    db.add(jwtblocklist)
    db.commit()
    return {'detail': 'Logged out successfully'}
