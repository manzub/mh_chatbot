import uvicorn


# @app.post('/send_love')
# async def send_love(params: Params):
#   result = "An error occurred"

#   if params.userId:
#     user = db.users.find_one({ "userId": params.userId }, { "_id": 0 })

#     if user: #found user
#       new_notification = Notification(notiId=shortuuid.uuid(), message=params.message, topic=params.topic) 
#       # update user notifications
#       user["notifications"].append(new_notification.dict())
#       db.users.update_one({ "userId": params.userId }, { "$set": { "notifications": user["notifications"] } })
#       result = "Updated"

#     else:
#       result = "Invalid user"

#   return JSONResponse(content=jsonable_encoder({ "response": result }))


# # TODO: revamp routes
# @app.post('/mark_noti_as_read')
# def mark_noti_as_read(params: Params):
#   if params.userId and params.notiId:
#     user = db.users.find_one({ "userId": params.userId }, { "_id": 0 })

#     if user:
#       for i, notification in enumerate(user["notifications"]):
#         if notification["notiId"] == params.notiId:
#           noti_item = user["notifications"][i]
#           noti_item["is_read"] = True
#           user["notifications"][i] = noti_item
#           break

#       db.users.update_one({ "userId": params.userId }, { "$set": { "notifications": user["notifications"] } })

#   # return result
#   return JSONResponse(content=jsonable_encoder({ "response": "success" }))


# @app.post('/delete_noti_item')
# def delete_noti_item(params: Params):
#   if params.userId and params.notiId:
#     user = db.users.find_one({ "userId": params.userId }, { "_id": 0 })

#     if user:
#       for i, notification in enumerate(user["notifications"]):
#         if notification["notiId"] == params.notiId:
#           del user["notifications"][i]
#           break

#       db.users.update_one({ "userId": params.userId }, { "$set": { "notifications": user["notifications"] } })

#   # return result
#   return JSONResponse(content=jsonable_encoder({ "response": "success" }))


# @app.post('/save_conversation') #if convoId
# def save_conversation(params: Params):
#   if params.userId and params.message:
#     messages = json.loads(params.message)
#     user = db.users.find_one({ "userId": params.userId }, { "_id": 0 })

#     if user: #found user
#       new_conversation = Conversation(convId=params.convId, messages=messages)

#       found_conversation = False
#       for i, item in enumerate(user["conversations"]):
#         print(item['convId'], params.convId)
#         if item['convId'] == params.convId:
#           found_conversation = True
#           # replace conversation else new conversation
#           user["conversations"][i] = new_conversation.dict()
#           break

#       if not found_conversation:
#         user["conversations"].append(new_conversation.dict())

#       db.users.update_one({ "userId": params.userId }, { "$set": { "conversations": user["conversations"] } })

#   # return result string
#   return JSONResponse(content=jsonable_encoder({ "response": "Updated", "messages": messages}))



if __name__ == "__main__":
  uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)