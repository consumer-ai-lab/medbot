from sqlalchemy import Column, Integer, String, Boolean
from .config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String,unique=True,index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean,default=False)


