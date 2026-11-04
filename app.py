import os
from flask import Flask, request, jsonify
from pymongo import MongoClient, ReadPreference
from pymongo.write_concern import WriteConcern

app = Flask(__name__)
db = MongoClient(os.environ["MONGO_URI"])["ev_db"]
vehicles = db["vehicles"]

@app.post("/insert-fast")
def insert_fast():
    collection = vehicles.with_options(write_concern=WriteConcern(w=1))
    result = collection.insert_one(request.get_json())
    return jsonify(inserted_id=str(result.inserted_id)), 201

@app.post("/insert-safe")
def insert_safe():
    collection = vehicles.with_options(write_concern=WriteConcern(w="majority"))
    result = collection.insert_one(request.get_json())
    return jsonify(inserted_id=str(result.inserted_id)), 201

@app.get("/count-tesla-primary")
def count_tesla():
    collection = vehicles.with_options(read_preference=ReadPreference.PRIMARY)
    return jsonify(count=collection.count_documents({"Make": "TESLA"}))

@app.get("/count-bmw-secondary")
def count_bmw():
    collection = vehicles.with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)
    return jsonify(count=collection.count_documents({"Make": "BMW"}))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
