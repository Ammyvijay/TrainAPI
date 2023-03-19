from typing import Union
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class PostModel(BaseModel):
    title:str
    content:str

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/createpost")
def createpost(payload:dict=Body(...)):
    print(payload)
    return {"info":"Successfully Created!"}

@app.post("/createposting")
def crepost(new_posts:PostModel):
    print(new_posts)
    return {"Okay"}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}