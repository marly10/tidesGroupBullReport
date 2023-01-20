from typing import *
from fastapi import *
from fastapi.responses import *
from fastapi.security import *
import secrets
from pydantic import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *
from pass_checker import *
from base_model import *


app = FastAPI()
security = HTTPBasic()


# GET username
def get_username(firstName):
    username = (
        DBSession.query(HostNameORM).filter(HostNameORM.firstName == firstName).first()
    )
    if username:
        print(username)
        return username
    else:
        return "entries"


# GET password
def get_password(PassWord):
    password = (
        DBSession.query(HostNameORM).filter(HostNameORM.PassWord == PassWord).first()
    )

    return password


def verify(credentials: HTTPBasicCredentials) -> None:
    correct_credentials = secrets.compare_digest(
        credentials.username + credentials.password, get_username() + get_password()
    )
    if not correct_credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

verify()
get_username("Tom")
