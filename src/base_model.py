from typing import *
from fastapi import *
from pydantic import *
from sqlalchemy import *
from sqlalchemy.orm import *

DB_HOST = "localhost"
DATABASE = "test_db"
engine = create_engine(f"mysql+pymysql://db_master:admin@{DB_HOST}/{DATABASE}")
# connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
DBSession = Session(engine)
DB_BASE_ORM = declarative_base()

# userId firstName lastName
class Name(BaseModel):
    userId: Optional[int] = None
    firstName: str
    lastName: str
    PassWord: str


class NameUpdate(BaseModel):
    userId: Optional[int] = None
    firstName: Optional[str]
    lastName: Optional[str]
    PassWord: Optional[str]


class HostNameORM(DB_BASE_ORM):
    __tablename__ = "test_table"
    userId = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String, index=False)
    lastName = Column(String, index=False)
    PassWord = Column(String, index=False)

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    password: str

# User: johndoe
# Password: secret hashed_password
