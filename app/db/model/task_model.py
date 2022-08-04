from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
import uuid
import datetime

def generate_uuid() -> str:
    """
    Generating the string type UUID

    :return: UUID in string
    """
    return str(uuid.uuid4())


# Model for the Task Table
class Task(Base):
    __tablename__ = 'task'
    task_id = Column(String, primary_key=True, index=True, default=generate_uuid)
    title = Column(String, index=True)
    description = Column(String)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.user_id'))

    created_by = relationship('User', back_populates='tasks')