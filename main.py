from typing import *
from fastapi import Query
from fastapi import *
from fastapi.responses import *
from pydantic import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *


app = FastAPI()

DB_HOST = "localhost" 
DATABASE = "test_db"
engine = create_engine(f"mysql+pymysql://db_master:admin@{DB_HOST}/{DATABASE}")
#connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
DBSession = Session(engine)
DB_BASE_ORM = declarative_base()

#userId firstName lastName
class Name(BaseModel):
    userId: Optional[int] = None
    firstName: str
    lastName: str

class NameUpdate(BaseModel):
    userId: Optional[int] = None
    firstName: Optional[str]
    lastName: Optional[str]
    
class HostNameORM(DB_BASE_ORM):
    __tablename__ = "test_table"
    userId = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String, index=False)
    lastName = Column(String, index=False)
    
# GET all the car records from the database
@app.get("/user-name")
def get_all_names(
    response: Response,
):
    try:
        name_records = DBSession.query(HostNameORM).filter().all()
        return {
            "entries": name_records,
            "total": len(name_records)
        }
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "entries": [],
            "total":0, 
            "error": e,
            "detail": e.orig.args if hasattr(e, 'orig') else f"{e}"
        }
        
# GET the car record from the database identified by RaceCarORM.id = car_id
@app.get("/user-name/{userId}")
def get_name(
    userId: int,
    request: Request,
    response: Response,
):
    try:
        host_name = DBSession.query(HostNameORM).filter(HostNameORM.userId == userId).first()
        if host_name:
            return {
                "entries": host_name,
            }
        else:
            return {
                "entries": [],
                "message": f"No entries found for id: {userId}"
            }
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "entries": [],
            "id_sent": host_name, 
            "total": 0,
            "error": e,
            "detail": e.orig.args if hasattr(e, 'orig') else f"{e}"
        }

# UPDATE the database record that is identified by RaceCarORM.id = race_car.id
@app.put("/user-name")
def edit_name(
    request: Request,
    response: Response,
    user_name: NameUpdate,
):
    message = ""
    try:
        if not user_name.userId:
            raise Exception("missing id")
        user_name_record = DBSession.query(HostNameORM).filter(HostNameORM.userId == user_name.userId).update(dict(user_name))                            
        message="Record correctly updated"
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        message = "{}".format(e)
    
    return {"car": user_name, "message": message}

# CREATE a new dabase record
@app.post("/user-name")
def create_user_name(
    request: Request,
    response: Response,
    user_name: Name,
):
    try:
        DBSession.begin()
        user_name_record = HostNameORM(**dict(user_name))
        DBSession.add(user_name_record)
        DBSession.commit()
        user_name.userId = user_name_record.userId
        return user_name
    except Exception as e:
        DBSession.rollback()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": e,
            "detail": e.orig.args if hasattr(e, 'orig') else f"{e}"
        }

#
# DELETE the record from the database that is idenfied by RaceCarORM.id = car_id
@app.delete("/user-name/{userId}")
def delete_user_name(
    request: Request,
    response: Response,
    userId: int
):
    try:
        num_rows = DBSession.query(HostNameORM).filter_by(userId=userId).delete()
        if num_rows == 0:
            raise HTTPException(status_code=404, detail="Record not found")
        DBSession.commit()
    except HTTPException as e:
        raise
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": e,
            "detail": e.orig.args if hasattr(e, 'orig') else f"{e}"
        }
    response.status_code = status.HTTP_204_NO_CONTENT
    return 

# def parse_list(names: List[str] = Query(None, description="List of names to greet")) -> Optional[List]:
    
#     def remove_prefix(text: str, prefix: str):
#         return text[text.startswith(prefix) and len(prefix):]

#     def remove_postfix(text: str, postfix: str):
#         if text.endswith(postfix):
#             text = text[:-len(postfix)]
#         return text

#     if names is None:
#         return

#     # we already have a list, we can return
#     if len(names) > 1:
#         return names

#     # if we don't start with a "[" and end with "]" it's just a normal entry
#     flat_names = names[0]
#     if not flat_names.startswith("[") and not flat_names.endswith("]"):
#         return names

#     flat_names = remove_prefix(flat_names, "[")
#     flat_names = remove_postfix(flat_names, "]")

#     names_list = flat_names.split(",")
#     names_list = [remove_prefix(n.strip(), "\"") for n in names_list]
#     names_list = [remove_postfix(n.strip(), "\"") for n in names_list]

#     return names_list


# @app.get("/name_array")
# def hello_list(names: List[str] = Depends(parse_list)):
#     """ 
#     --> list param method \n
#       --> accepts strings formatted as lists with square brackets \n
#       --> names can be in the format \n
#       --> "[bob,jeff,greg]" or '["bob","jeff","greg"]'
#     """

#     if names is not None:
#         return StreamingResponse((f"Hello {name}\n" for name in names))
#     else:
#         return {"message": "no names"}

# class GraphBase(BaseModel):
#     start: str
#     end: str
#     distance: int

# class UserName(BaseModel):
#     first_name: str
#     last_name: str
#     age: int
    
# UserNameData = [
#     {"first_name": "Foo", "last_name": "jack", "age": 22},
#      {"first_name": "test", "last_name": "dave", "age": 43},
# ]

# class GraphList(BaseModel):
#     data: List[GraphBase]

# @app.get("/getnames", response_model=List[UserName])
# async def get_body():
#     return UserNameData

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
