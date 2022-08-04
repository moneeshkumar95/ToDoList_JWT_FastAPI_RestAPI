from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.base import User, get_db, JwtBlocklist
import uuid


# For JWT configuration
SECRET_KEY = "05d25e094faa6ca2556c515166b7a9563b93f7099f650f4caa6cf63b8858d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(days=1)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/login")


def create_access_token(data: dict) -> str:
    """
    For the generating the access_token or refresh_token

    :param data: sub-> user_id
    :return: JWT token
    """
    data.update({"exp": datetime.utcnow() + ACCESS_TOKEN_EXPIRE,
                 'jti': str(uuid.uuid4()),
                 "type": 'access'})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


async def auth_required(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> dict:
    """
    For checking the JWT token is valid

    :return: parsed token data
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Login expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti: str = payload['jti']
    except (JWTError, KeyError):
        raise credentials_exception

    jwtblocklist = db.query(JwtBlocklist).filter(JwtBlocklist.jti == jti).first()

    if jwtblocklist:
        raise credentials_exception

    return payload


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    For checking the JWT token & get the current user data

    :return: User data
    """
    data = await auth_required(token=token, db=db)
    user = db.query(User).filter(User.user_id == data['sub']).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return user