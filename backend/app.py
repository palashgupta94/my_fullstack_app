
import os
import json
import uuid
import time
import threading
import logging
import signal
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import certifi

# Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
load_dotenv()

# Environment variables
MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME")
JSON_FALLBACK_PATH = os.getenv("JSON_FALLBACK_PATH", "/data/fallback_data.json")

# Validate environment variables
if not all([MONGODB_ATLAS_URI, DB_NAME, COLLECTION_NAME]):
    logger.error("Missing required environment variables: MONGODB_ATLAS_URI, DB_NAME, COLLECTION_NAME")
    sys.exit(1)

# Globals
mongo_connected = False
client = db = collection = None
file_lock = threading.Lock()

# Connect to Mongo
def try_connect_to_mongo():
    global mongo_connected, client, db, collection
    try:
        logger.debug("Attempting MongoDB connection...")
        client = MongoClient(
            MONGODB_ATLAS_URI,
            serverSelectionTimeoutMS=10000,
            server_api=ServerApi('1'),
            tlsCAFile=certifi.where() if "mongodb+srv" in MONGODB_ATLAS_URI else None
        )
        client.server_info()
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        mongo_connected = True
        logger.info("Connected to MongoDB.")
    except Exception as e:
        mongo_connected = False
        logger.error("MongoDB connection failed:")

try_connect_to_mongo()

# JSON fallback helpers
def ensure_data_dir():
    os.makedirs(os.path.dirname(JSON_FALLBACK_PATH), exist_ok=True)

def get_from_json():
    with file_lock:
        try:
            ensure_data_dir()
            if not os.path.exists(JSON_FALLBACK_PATH):
                return []
            with open(JSON_FALLBACK_PATH, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.exception("Error reading JSON:")
            return []

def save_all_to_json(data_list):
    with file_lock:
        ensure_data_dir()
        temp_path = JSON_FALLBACK_PATH + ".tmp"
        try:
            with open(temp_path, "w") as f:
                json.dump(data_list, f, indent=4)
            os.replace(temp_path, JSON_FALLBACK_PATH)
        except Exception as e:
            logger.exception("Error saving JSON:")
            raise

def get_item_from_json(item_id):
    return next((item for item in get_from_json() if item.get("id") == item_id), None)

def save_to_json(data):
    items = get_from_json()
    items.append(data)
    save_all_to_json(items)

# Background threads
def monitor_mongo_connection():
    global mongo_connected
    while True:
        if not mongo_connected:
            logger.info("Mongo down. Retrying connection...")
            try_connect_to_mongo()
        else:
            try:
                client.admin.command('ping')
            except:
                mongo_connected = False
                logger.warning("MongoDB connection lost.")
        time.sleep(10)

def sync_fallback_to_mongo():
    while True:
        if mongo_connected:
            try:
                fallback_data = get_from_json()
                synced_count = 0
                for item in fallback_data:
                    if "_id" in item and isinstance(item["_id"], dict) and "$oid" in item["_id"]:
                        item["_id"] = item["_id"]["$oid"]
                    if not collection.find_one({"id": item["id"]}):
                        collection.insert_one(item)
                        synced_count += 1
                logger.info(f"Synced {synced_count} new fallback items to Mongo.")
            except Exception as e:
                logger.warning(f"Sync error: {e}")
        time.sleep(30)

def is_mongo_usable():
    return mongo_connected

# Handle shutdown
def shutdown_handler(sig, frame):
    logger.info("Received shutdown signal, closing MongoDB client...")
    if client:
        client.close()
    logger.info("Shutdown complete.")
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)

# REST API
@app.route("/api/items", methods=["GET"])
def get_all_items():
    try:
        if is_mongo_usable():
            return jsonify(list(collection.find({}, {"_id": 0})))
        return jsonify(get_from_json())
    except Exception as e:
        logger.exception("GET /api/items failed:")
        return jsonify({"error": str(e)}), 500

@app.route("/api/items/<item_id>", methods=["GET"])
def get_item(item_id):
    try:
        if is_mongo_usable():
            item = collection.find_one({"id": item_id}, {"_id": 0})
            return jsonify(item) if item else (jsonify({"error": "Not found"}), 404)
        item = get_item_from_json(item_id)
        return jsonify(item) if item else (jsonify({"error": "Not found"}), 404)
    except Exception as e:
        logger.exception("GET /api/items/<id> failed:")
        return jsonify({"error": str(e)}), 500

@app.route("/api/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    try:
        if is_mongo_usable():
            result = collection.update_one({"id": item_id}, {"$set": data})
            if result.matched_count:
                return jsonify({"message": "Updated"})
            return jsonify({"error": "Not found"}), 404
        items = get_from_json()
        for idx, item in enumerate(items):
            if item["id"] == item_id:
                items[idx].update(data)
                save_all_to_json(items)
                return jsonify({"message": "Updated fallback"})
        return jsonify({"error": "Not found"}), 404
    except Exception as e:
        logger.exception("PUT /api/items/<id> failed:")
        return jsonify({"error": str(e)}), 500

@app.route("/api/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    try:
        mongo_deleted = False
        file_deleted = False
        if is_mango_usable():
            result = collection.delete_one({"id": item_id})
            mongo_deleted = result.deleted_count > 0
        items = get_from_json()
        new_items = [item for item in items if item.get("id") != item_id]
        if len(new_items) < len(items):
            save_all_to_json(new_items)
            file_deleted = True
        if mongo_deleted or file_deleted:
            deleted_from = []
            if mongo_deleted:
                deleted_from.append("MongoDB")
            if file_deleted:
                deleted_from.append("fallback")
            return jsonify({"message": f"Deleted from {', '.join(deleted_from)}"})
        return jsonify({"error": "Item not found in MongoDB or fallback"}), 404
    except Exception as e:
        logger.exception("DELETE /api/items/<id> failed:")
        return jsonify({"error": str(e)}), 500

@app.route("/api/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json(force=True)
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        data["_id"] = data["id"]
        if is_mongo_usable():
            try:
                collection.insert_one(data)
                data.pop("_id", None)
                logger.info(f"Inserted item to MongoDB: {data['id']}")
                return jsonify({"status": "success", "storage": "mongodb", "data": data}), 201
            except Exception as e:
                logger.exception(f"MongoDB insert failed for id={data['id']}:")
                logger.warning("Falling back to JSON storage.")
        save_to_json(data)
        data.pop("_id", None)
        logger.info(f"Saved item to JSON fallback: {data['id']}")
        return jsonify({"status": "success", "storage": "fallback", "data": data}), 201
    except Exception as e:
        logger.exception("POST /api/submit failed:")
        return jsonify({"error": str(e)}), 500

# Start app
threading.Thread(target=monitor_mongo_connection, daemon=True).start()
threading.Thread(target=sync_fallback_to_mongo, daemon=True).start()

if __name__ == "__main__":
    logger.info("Flask app running at http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)