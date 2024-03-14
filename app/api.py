import json
import shortuuid
import contextlib
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Query, Depends
from app.model import User, Notification, Conversation, Params
from app.auth.auth_handler import signJWT
from app.auth.auth_bearer import JWTBearer
from pymongo import MongoClient
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from bot import chatbot_response

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

def api_response(message: str = None, status: str = None, data: dict | list = None):
  return {
    "status": status,
    "message": message,
    "data": data
  }

def check_user(userId: str):
  user = db.users.find_one({ "userId": userId }, { "_id": 0 })
  if user:
    return True
  else:
    return False


@app.get("/", tags=["root"])
async def read_root() -> dict:
  return JSONResponse(content=api_response(status="success", message="Welcome"))


@app.get("/topics", tags=["root"])
async def get_topics():
  topics = ["send love", "focus"]
  return JSONResponse(content=api_response(status="success", data=topics))


@app.get("/mindfulcards", tags=["root"])
async def get_mindfulcards():
  mindfulcards = db.mindfulcards.find({}, { "_id": False })
  return JSONResponse(content=api_response(status="success", data=list(mindfulcards)))


@app.post('/auth/new_token', tags=["auth"])
async def new_token(userId: str):
  if check_user(userId):
    return JSONResponse(content=api_response(status="success", data=signJWT(userId)))
  return JSONResponse(content=api_response(status="error", message="Invalid user!"))


@app.get('/setup_oom_user', tags=["auth"])
async def setup_oom_user():
  # setup unique user id
  userId = shortuuid.uuid()
  result = User(_id=ObjectId(), userId=userId, notifications=[], conversations=[])
  # check exists user
  user = db.users.find_one({ "userId": userId }, { "_id": 0 })

  if user: #if found a user - create a new uuid
    result['userId'] = shortuuid.uuid()

  db.users.insert_one(result.dict(by_alias=True))
  return JSONResponse(content=api_response(status="success", message="Registered new device", data=jsonable_encoder(result)))


@app.get('/get_user/{userId}', tags=["user"])
async def get_user_by_id(userId: str):
  result = "An error occurred"
  status = "error"
  user = db.users.find_one({ "userId": userId }, { "_id": 0 })

  if user:
    status = "success"
    result = "User found"
  else:
    result = "User not found"
    
  return JSONResponse(content=api_response(status=status, message=result, data=jsonable_encoder(user)))


@app.post('/send_love', dependencies=[Depends(JWTBearer())], tags=["actions", "notifications"])
async def send_love(params: Params):
  message = "An error occurred"
  status = "error"
  user = db.users.find_one({ "userId": params.userId }, { "_id": 0 })

  if user:
    new_notification = Notification(notiId=shortuuid.uuid(), message=params.message, topic=params.topic)
    # update user notifications
    user["notifications"].append(new_notification.dict())
    db.users.update_one({ "userId": params.userId }, { "$set": { "notifications": user["notifications"] } })
    message = "Updated"
    status = "success"
  else:
    message = "Invalid user"

  return JSONResponse(content=api_response(status=status, message=message))


@app.post('/mark_noti_as_read', dependencies=[Depends(JWTBearer())], tags=["notifications"])
async def mark_noti_as_read(params: Params):
  if params.userId and params.notiId:
    user = db.users.find_one({ "userId": params.userId }, { "_id": 0 })
    if user:
      for i, notifications in enumerate(user["notifications"]):
        if notifications["notiId"] == params.notiId:
          noti_item = user["notifications"][i]
          noti_item["is_read"] = True
          user["notifications"][i] = noti_item
          break
      db.users.update_one({ "userId": params.userId }, { "$set": { "notifications": user["notifications"] } })
  return JSONResponse(content=api_response(status="success"))


@app.post('/delete_noti_item', dependencies=[Depends(JWTBearer())], tags=["notifications"])
async def delete_noti_item(params: Params):
  if params.userId and params.notiId:
    user = db.users.find_one({ "userId": params.userId }, { "_id": 0 })
    if user:
      for i, notifications in enumerate(user["notifications"]):
        if notifications["notiId"] == params.notiId:
          del user["notifications"][i]
          break
      db.users.update_one({ "userId": params.userId }, { "$set": { "notifications": user["notifications"] } })
  return JSONResponse(content=api_response(status="success"))


@app.post('/response', dependencies=[Depends(JWTBearer())], tags=["ml-ai"])
def get_bot_response(params: Params):
  userText = params.message
  response = chatbot_response(userText, params.userId)
  return JSONResponse(content=api_response(status="success", message=response))


@app.post('/save_conversation', dependencies=[Depends(JWTBearer())], tags=["ml-ai"])
async def save_conversation(params: Params):
  if params.userId and params.message:
    messages = json.loads(params.message)
    user = db.users.find_one({ "userId": params.userId }, { "_id": 0 })

    if user:
      new_conversation = Conversation(convId=params.convId, messages=messages)
      found_conversation = False
      for i, item in enumerate(user["conversations"]):
        print(item['convId'], params.convId)
        if item['convId'] == params.convId:
          found_conversation = True
          # replace conversation else new conversation
          user["conversations"][i] = new_conversation.dict()
          break

      if not found_conversation:
        user["conversations"].append(new_conversation.dict())

      db.users.update_one({ "userId": params.userId }, { "$set": { "conversations": user["conversations"] } })

  # return result string
  return JSONResponse(content=api_response(status="success", data=messages))

