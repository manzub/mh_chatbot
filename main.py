import uvicorn


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