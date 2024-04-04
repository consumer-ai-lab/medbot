from sqlalchemy import Column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String
from .config import Base
from .schemas import UserLevel


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,index=True)
    email = Column(String, unique=True,index=True)
    user_name = Column(String)
    user_level = Column(SQLEnum(UserLevel))
    hashed_password = Column(String)    


