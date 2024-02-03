""" 
Script to parse app information from mindfulcards.json, create the appropriate databases and
collection(s) on a local instance of MongoDB, create the appropriate indices (for efficient retrieval)
and finally add the course data on the collection(s).
"""

import pymongo
import json

# connect to mongodb
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['oom']
collection = db['mindfulcards']

# read courses from json
with open("mindfulcards.json", "r") as f:
  mindfulcards = json.load(f)

# Create index for efficient retrieval
collection.create_index("title")

for item in mindfulcards:
  collection.insert_one(item)

# close connection
  client.close()