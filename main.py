from typing import Union
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from enum import Enum
from dataclasses import dataclass
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import time
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@dataclass
class PostModel(BaseModel):
    title: str
    content: str


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

while True:

    try:

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')

        conn = psycopg2.connect(host=os.getenv('host'), database=os.getenv('database'),
                                user=os.getenv('user'), password=os.getenv('password'),
                                cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("Postgres DB is connected Successfully!")
        break
    except Exception as e:
        print("Error : ", e)
        time.sleep(5)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/getpost")
def getpost():
    posts = None
    try:
        cur.execute("""SELECT * from posts""")
        posts = cur.fetchall()
        print(posts)
    except Exception as e:
        print("Error : ", e)
    return {"info": posts}


@app.post("/createpost")
def createpost(payload: dict = Body(...)):
    print(payload)
    return {"info": "Successfully Created!"}


@app.post("/createposting")
def crepost(new_posts: PostModel):
    print(new_posts)
    return {"Okay"}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
