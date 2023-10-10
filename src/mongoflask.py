from flask import Flask, jsonify, request
import isodate as iso
from datetime import date, datetime
from bson import ObjectId
from flask.json import JSONEncoder
from werkzeug.routing import BaseConverter

app = Flask(__challenge__)
# JSON encoder to handle custom types
class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return iso.datetime_isoformat(o)
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super().default(o)

# Custom converter for change type ObjectId
class ObjectIdConverter(BaseConverter):
    def to_python(self, value):
        return ObjectId(value)

    def to_url(self, value):
        return str(value)

# Replace with the mongo connection (NOT SET YET)
# Import the MongoClient at the top of your script
from pymongo import MongoClient

# Initialize the MongoDB client with your connection string
# mongo = MongoClient("mongodb://connection-not-set")

# Modify the endpoint to return JSON by id or All restaurants
@app.route('/api/v1/restaurant/<id>', methods=['GET'])
def get_restaurant_by_id(id):
    if id:
        restaurant = find_restaurant_by_id(id)
        if restaurant:
            return jsonify(restaurant)
        else:
            return ('', 204)
    else:
        restaurants = find_all_restaurants()
        if restaurants:
            return jsonify(restaurants)
        else:
            return ('', 204)

# Function to return by ID
def find_restaurant_by_id(id):
    restaurant = mongo.db.restaurant.find_one({"_id": ObjectId(id)})
    return restaurant  # Replace with your actual query

# Function to return All restaurants
def find_all_restaurants():
    restaurants = list(mongo.db.restaurant.find())
    return restaurants

if __challenge__ == '__main__':
    app.run(debug=True)
