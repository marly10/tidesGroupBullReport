from typing import *
from fastapi import *
from fastapi.responses import *
from fastapi.security import *
from pydantic import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *
from slack import *
from auth import *
from json_test import *
from base_model import *
#https://mixedanalytics.com/blog/list-actually-free-open-no-auth-needed-apis/

app = FastAPI()
security = HTTPBasic()
webhook = (
    "https://hooks.slack.com/services/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"
)


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = json_return(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# GET all the car records from the database
@app.get("/user-name")
def get_all_names(response: Response = Depends(get_current_active_user)):
    try:
        # sends information to slack channel
        payload = {"text": "Someone has called all the data stored in the database!"}
        send_slack_message(payload, webhook)

        name_records = DBSession.query(HostNameORM).filter().all()
        return {"entries": name_records, "total": len(name_records)}
    except Exception as e:
        # sends information to slack channel
        payload = {"text": "Someone has tried to access info from db, but it failed!"}
        send_slack_message(payload, webhook)

        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "entries": [],
            "total": 0,
            "error": e,
            "detail": e.orig.args if hasattr(e, "orig") else f"{e}",
        }


# GET the car record from the database identified by RaceCarORM.id = car_id
@app.get("/user-name/{userId}")
def get_name(
    userId: int, request: Request, response: Response = Depends(get_current_active_user)
):
    try:
        # sends information to slack channel
        slack_string = f"user with id: {userId} has been called!"
        payload = {"text": slack_string}
        send_slack_message(payload, webhook)

        host_name = (
            DBSession.query(HostNameORM).filter(HostNameORM.userId == userId).first()
        )
        if host_name:
            return {
                "entries": host_name,
            }
        else:
            return {"entries": [], "message": f"No entries found for id: {userId}"}
    except Exception as e:
        # sends information to slack channel
        slack_string = f"user with id: {userId} has been called, but not found!"
        payload = {"text": slack_string}
        send_slack_message(payload, webhook)

        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "entries": [],
            "id_sent": host_name,
            "total": 0,
            "error": e,
            "detail": e.orig.args if hasattr(e, "orig") else f"{e}",
        }


# UPDATE the database record that is identified by RaceCarORM.id = race_car.id
@app.put("/user-name")
def edit_name(
    request: Request,
    response: Response,
    user_name: NameUpdate = Depends(get_current_active_user),
):
    message = ""
    try:
        # sends information to slack channel
        slack_string = f"user: {user_name.firstName} has been called!"
        payload = {"text": slack_string}
        send_slack_message(payload, webhook)

        if not user_name.userId:
            raise Exception("missing id")
        user_name_record = (
            DBSession.query(HostNameORM)
            .filter(HostNameORM.userId == user_name.userId)
            .update(dict(user_name))
        )
        message = "Record correctly updated"
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        message = "{}".format(e)

    return {"car": user_name, "message": message}


# CREATE a new dabase record
@app.post("/user-name")
def create_user_name(
    request: Request,
    response: Response,
    user_name: Name = Depends(get_current_active_user),
):
    try:
        # sends information to slack channel
        slack_string = f"A user with f_name: {user_name.firstName}, l_name: {user_name.lastName} has been created!"
        payload = {"text": slack_string}
        send_slack_message(payload, webhook)

        DBSession.begin()
        user_name_record = HostNameORM(**dict(user_name))
        DBSession.add(user_name_record)
        DBSession.commit()
        user_name.userId = user_name_record.userId
        return user_name

    except Exception as e:
        DBSession.rollback()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": e, "detail": e.orig.args if hasattr(e, "orig") else f"{e}"}


#
# DELETE the record from the database that is idenfied by RaceCarORM.id = car_id
@app.delete("/user-name/{userId}")
def delete_user_name(
    request: Request, response: Response, userId: int = Depends(get_current_active_user)
):
    try:
        # sends information to slack channel
        get_name(userId, request, response)
        slack_string = f"A user with id:{userId} has been deleted!"
        payload = {"text": slack_string}
        send_slack_message(payload, webhook)
        num_rows = DBSession.query(HostNameORM).filter_by(userId=userId).delete()
        if num_rows == 0:
            raise HTTPException(status_code=404, detail="Record not found")
        DBSession.commit()
    except HTTPException as e:
        raise
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": e, "detail": e.orig.args if hasattr(e, "orig") else f"{e}"}
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
