import os
import json
import uuid
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId, json_util
from dotenv import load_dotenv
import certifi

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins="*")

logger.info("Loading environment variables...")
load_dotenv()

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME")
JSON_FALLBACK_PATH = "/data/fallback_data.json"

logger.info(f"MONGODB_ATLAS_URI: {MONGODB_ATLAS_URI}")
logger.info(f"DB_NAME: {DB_NAME}")
logger.info(f"COLLECTION_NAME: {COLLECTION_NAME}")
logger.info(f"JSON_FALLBACK_PATH: {JSON_FALLBACK_PATH}")

mongo_connected = False
client, db, collection = None, None, None

def try_connect_to_mongo():
    global mongo_connected, client, db, collection
    logger.info("Attempting to connect to MongoDB Atlas...")
    try:
        if "mongodb+srv" in MONGODB_ATLAS_URI:
            client = MongoClient(
                MONGODB_ATLAS_URI,
                serverSelectionTimeoutMS=3000,
                server_api=ServerApi('1'),
                tlsCAFile=certifi.where()
            )
        else:
            client = MongoClient(
                MONGODB_ATLAS_URI,
                serverSelectionTimeoutMS=3000,
                server_api=ServerApi('1')
            )

        client.server_info()  # Trigger connection
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        mongo_connected = True
        logger.info("Successfully connected to MongoDB Atlas.")
    except Exception as e:
        mongo_connected = False
        logger.error("MongoDB connection failed: ")
        if logger.isEnabledFor(logging.DEBUG):
            logger.exception(e)

# Initial connection check at startup
try_connect_to_mongo()

# Helper Functions
def ensure_data_dir():
    os.makedirs(os.path.dirname(JSON_FALLBACK_PATH), exist_ok=True)

def get_from_json():
    try:
        logger.info("Loading data from fallback JSON...")
        ensure_data_dir()
        if not os.path.exists(JSON_FALLBACK_PATH):
            logger.warning("Fallback file does not exist.")
            return []
        with open(JSON_FALLBACK_PATH, "r") as f:
            data = json.load(f, object_hook=json_util.object_hook)
            logger.info("Loaded fallback data.")
            return data if isinstance(data, list) else [data] if isinstance(data, dict) else []
    except Exception as e:
        logger.exception("Error reading JSON fallback:")
        return []

def save_all_to_json(data_list):
    try:
        logger.info("Saving all data to fallback JSON...")
        ensure_data_dir()
        with open(JSON_FALLBACK_PATH, "w") as f:
            json.dump(data_list, f, indent=4, default=json_util.default)
        logger.info("Data saved to fallback JSON.")
    except Exception as e:
        logger.exception("Error saving to JSON fallback:")
        raise

def get_item_from_json(id):
    try:
        logger.info(f"Getting item with ID {id} from fallback JSON...")
        items = get_from_json()
        return next((i for i in items if i.get("id") == id), None)
    except Exception as e:
        logger.exception("Error finding item in JSON:")
        return None

def save_to_json(data):
    try:
        logger.info("Saving new item to fallback JSON...")
        ensure_data_dir()
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        items = get_from_json()
        items.append(data)
        save_all_to_json(items)
    except Exception as e:
        logger.exception("Error saving item to JSON:")
        raise

# Endpoints
@app.route("/api/items", methods=["GET"])
def get_all_items():
    logger.info("Endpoint hit: GET /api/items")
    try:
        try_connect_to_mongo()
        if mongo_connected:
            try:
                logger.info("Fetching items from MongoDB...")
                items = list(collection.find({}, {"_id": 0}))
                return jsonify(items)
            except Exception as e:
                logger.exception("MongoDB error:")
        logger.warning("Falling back to JSON data...")
        return jsonify(get_from_json())
    except Exception as e:
        logger.exception("Error in GET /api/items:")
        return jsonify({"error": str(e)}), 500

@app.route("/api/items/<id>", methods=["GET"])
def get_item(id):
    logger.info(f"Endpoint hit: GET /api/items/{id}")
    try:
        try_connect_to_mongo()
        if mongo_connected:
            try:
                logger.info(f"Fetching item {id} from MongoDB...")
                item = collection.find_one({"_id": ObjectId(id)}, {"_id": 0})
                return jsonify(item) if item else (jsonify({"error": "Not found"}), 404)
            except Exception as e:
                logger.exception("MongoDB error:")
        logger.warning("Falling back to JSON...")
        item = get_item_from_json(id)
        return jsonify(item) if item else (jsonify({"error": "Not found"}), 404)
    except Exception as e:
        logger.exception("Error in GET /api/items/<id>:")
        return jsonify({"error": str(e)}), 500

@app.route("/api/items/<id>", methods=["PUT"])
def update_item(id):
    logger.info(f"Endpoint hit: PUT /api/items/{id}")
    try:
        data = request.json
        try_connect_to_mongo()
        if mongo_connected:
            try:
                logger.info(f"Updating item {id} in MongoDB...")
                result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
                if result.modified_count:
                    return jsonify({"message": "Item updated"})
                else:
                    return jsonify({"error": "Not found"}), 404
            except Exception as e:
                logger.exception("MongoDB error:")
        logger.warning("Falling back to JSON...")
        items = get_from_json()
        item_idx = next((i for i, item in enumerate(items) if item.get("id") == id), None)
        if item_idx is None:
            return jsonify({"error": "Not found"}), 404
        items[item_idx].update(data)
        save_all_to_json(items)
        return jsonify({"message": "Item updated (fallback)"})
    except Exception as e:
        logger.exception("Error in PUT /api/items/<id>:")
        return jsonify({"error": str(e)}), 500

@app.route("/api/items/<id>", methods=["DELETE"])
def delete_item(id):
    logger.info(f"Endpoint hit: DELETE /api/items/{id}")
    try:
        try_connect_to_mongo()
        if mongo_connected:
            try:
                logger.info(f"Deleting item {id} from MongoDB...")
                result = collection.delete_one({"_id": ObjectId(id)})
                if result.deleted_count:
                    return jsonify({"message": "Item deleted"})
                else:
                    return jsonify({"error": "Not found"}), 404
            except Exception as e:
                logger.exception("MongoDB error:")
        logger.warning("Falling back to JSON...")
        items = get_from_json()
        new_items = [item for item in items if item.get("id") != id]
        if len(items) == len(new_items):
            return jsonify({"error": "Not found"}), 404
        save_all_to_json(new_items)
        return jsonify({"message": "Item deleted (fallback)"})
    except Exception as e:
        logger.exception("Error in DELETE /api/items/<id>:")
        return jsonify({"error": str(e)}), 500

@app.route("/api/submit", methods=["POST"])
def submit():
    logger.info("Endpoint hit: POST /api/submit")
    try:
        data = request.get_json(force=True)
        logger.info(f">>> Parsed request data: {data}")
        try_connect_to_mongo()
        if mongo_connected:
            try:
                logger.info("Inserting new item into MongoDB...")
                result = collection.insert_one(data)
                logger.info(f"Inserted item with ID: {result.inserted_id}")

                response_data = data.copy()
                response_data["id"] = str(result.inserted_id)
                response_data.pop("_id", None)  # Just in case
                return jsonify({"status": "success", "data": response_data}), 201
            except Exception as e:
                logger.exception("Error saving to MongoDB:")
        logger.warning("Falling back to JSON storage...")
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        if "_id" in data:
            data["_id"] = str(data["_id"])
        save_to_json(data)
        return jsonify({"status": "fallback", "data": data}), 201
    except Exception as e:
        logger.exception("Submit error:")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logger.info("Starting Flask app on http://0.0.0.0:5000 ...")
    app.run(host="0.0.0.0", port=5000, debug=True)
