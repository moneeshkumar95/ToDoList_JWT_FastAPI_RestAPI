from fastapi import FastAPI
from db.base import Base
from db.database import engine
from apis.base import router


def create_table() -> None:
    """
    For creating tables only exist in DB

    :return: None
    """
    Base.metadata.create_all(bind=engine)


def start_application() -> FastAPI:
    """
    For creating the FastAPI instance, including the all path into instance & table creation
    
    :return: FastAPI instance
    """
    app_inst = FastAPI()
    app_inst.include_router(router)
    create_table()
    return app_inst

app = start_application()

