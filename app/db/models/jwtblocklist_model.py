from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from ..database import Base


# Model for the JWT token BlockList Table
class JwtBlocklist(Base):
    __tablename__ = 'jwtblocklist'
    jti = Column(String, primary_key=True, index=True)
    ttl = Column(DateTime)
