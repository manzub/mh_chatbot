from bot import chatbot_response
import contextlib
from fastapi import FastAPI, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
  msg: str


@app.get('/')
def root():
  return {"Hello": "World"}

@app.post('/response')
def get_bot_response(item: Item):
  userText = item.msg
  return chatbot_response(userText, '123')