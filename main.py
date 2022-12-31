from typing import *
from fastapi import *
from fastapi.responses import *
from pydantic import *

app = FastAPI()

def parse_list(names: List[str] = Query(None, description="List of names to greet")) -> Optional[List]:
    """
    accepts strings formatted as lists with square brackets
    names can be in the format
    "[bob,jeff,greg]" or '["bob","jeff","greg"]'
    """
    def remove_prefix(text: str, prefix: str):
        return text[text.startswith(prefix) and len(prefix):]

    def remove_postfix(text: str, postfix: str):
        if text.endswith(postfix):
            text = text[:-len(postfix)]
        return text

    if names is None:
        return

    # we already have a list, we can return
    if len(names) > 1:
        return names

    # if we don't start with a "[" and end with "]" it's just a normal entry
    flat_names = names[0]
    if not flat_names.startswith("[") and not flat_names.endswith("]"):
        return names

    flat_names = remove_prefix(flat_names, "[")
    flat_names = remove_postfix(flat_names, "]")

    names_list = flat_names.split(",")
    names_list = [remove_prefix(n.strip(), "\"") for n in names_list]
    names_list = [remove_postfix(n.strip(), "\"") for n in names_list]

    return names_list


@app.get("/hello_list")
def hello_list(names: List[str] = Depends(parse_list)):
    """ list param method """

    if names is not None:
        return StreamingResponse((f"Hello {name}\n" for name in names))
    else:
        return {"message": "no names"}

class GraphBase(BaseModel):
    start: str
    end: str
    distance: int

class GraphList(BaseModel):
    data: List[GraphBase]

@app.post("/dummypath")
async def get_body(data: GraphList):
    return data

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
