import certifi
from flask import Flask, request, jsonify, logging
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
CORS(app, origins="*")

client = MongoClient("mongodb+srv://palashgupta94:har23071990@cluster0.qrhlii4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client['mydatabase']
collection = db['mycollection']

@app.route('/process', methods=['POST'])
def submit_form_details():

    print("getting details")
    data = request.json
    print(f"data: ", data)
    username = data['username']
    email = data['email']
    print(f"user name: {username}, email: {email}")
    collection.insert_one({'username': username, 'email': email})
    return jsonify({"status": "success", "username": username, "email": email})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
