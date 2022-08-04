from sqlalchemy import Column, Integer, String, DateTime, BLOB
from sqlalchemy.orm import relationship
from ..database import Base
import datetime
import uuid
from bcrypt import hashpw, checkpw, gensalt

def generate_uuid() -> str:
    """
    Generating the string type UUID

    :return: UUID in string
    """
    return str(uuid.uuid4())

# Model for the Task Table
class User(Base):
    __tablename__ = 'user'
    user_id = Column(String, primary_key=True, index=True, default=generate_uuid)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, index=True, unique=True)
    email = Column(String, index=True, unique=True)
    hash_password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    tasks = relationship('Task', back_populates='created_by')

    @property
    def password(self):
        raise Exception('Your not allowed to view password')

    @password.setter
    def password(self, plain_password):
        self.hash_password = hashpw(plain_password.encode('utf-8'), gensalt())

    def verify_password(self, plain_password):
        return checkpw(password=plain_password.encode('utf-8'),
                       hashed_password=self.hash_password)