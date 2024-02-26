from bot import chatbot_response
from models import User, Notification, Conversation
import json
import shortuuid
import contextlib
from fastapi import FastAPI, HTTPException, Query
from bson import ObjectId
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


origins = [
  "http://localhost:3000"
]

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_headers=["*"],
  allow_methods=["*"],
)

client = MongoClient('mongodb://localhost:27017/')
db = client['oom']


@app.get('/')
def root():
  return {"Hello": "World"}

@app.get('/setup_oom_user')
async def setup_oom_user():
  # setup unique user id
  userId = shortuuid.uuid()
  result = User(_id=ObjectId(), userId=userId, notifications=[])
  # check exists user
  user = db.users.find_one({ "userId": userId }, { "_id": 0 })

  if user: #if found a user - create a new uuid
    result['userId'] = shortuuid.uuid()

  db.users.insert_one(result.dict(by_alias=True))
  return JSONResponse(content=jsonable_encoder(result))

@app.get('/get_user/{userId}')
async def get_user_by_id(userId: str):
  result = "An error occured"

  if userId:
    user = db.users.find_one({ "userId": userId }, { "_id": 0 })

    if user:
      result = "User found"
    else:
      result = "User not found"

  return JSONResponse(content=jsonable_encoder({ "response": result, "user": user }))


class Params(BaseModel):
  userId: str
  message: str
  convId: str | None = None
  topic: str | None = None

@app.post('/send_love')
async def send_love(params: Params):
  result = "An error occurred"

  if params.userId:
    user = db.users.find_one({ "userId": params.userId }, { "_id": 0 })

    if user: #found user
      new_notification = Notification(message=params.message, topic=params.topic) 
      # update user notifications
      user["notifications"].append(new_notification.dict())
      db.users.update_one({ "userId": params.userId }, { "$set": { "notifications": user["notifications"] } })
      result = "Updated"

    else:
      result = "Invalid user"

  return JSONResponse(content=jsonable_encoder({ "response": result }))


@app.post('/save_conversation') #if convoId
def save_conversation(params: Params):
  if params.userId and params.message:
    messages = json.loads(params.message)
    user = db.users.find_one({ "userId": params.userId }, { "_id": 0 })

    if user: #found user
      new_conversation = Conversation(convId=params.convId, messages=messages)

      found_conversation = False
      for i, item in user["conversations"]:
        if item['convId'] == params.convId:
          found_conversation = True
          # replace conversation else new conversation
          user["conversations"][i] = new_conversation.dict()
          break

      if not found_conversation:
        user["conversations"].append(new_conversation.dict())

      db.users.update_one({ "userId": params.userId }, { "$set": { "conversations": user["conversations"] } })

  # return result string
  return JSONResponse(content=jsonable_encoder({ "response": "Updated", "messages": messages}))


@app.post('/response')
def get_bot_response(params: Params):
  userText = params.message
  return chatbot_response(userText, '123')