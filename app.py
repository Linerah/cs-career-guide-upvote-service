import json

from bson import json_util
from flask import Flask, request
import pymongo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

app.config['MONGO_DBNAME'] = 'user_auth'

client = pymongo.MongoClient(
    "mongodb+srv://admin:NtXLrfmOBLhl00bm@capstoneauth.25mmcqj.mongodb.net/?retryWrites=true&w=majority", tls=True,
    tlsAllowInvalidCertificates=True)
db = client['user-auth']


@app.route("/upvote", methods=['POST', 'GET'])
@cross_origin()
def upvote():
    if request.method == "POST":
        value = request.json['value']
        blog_id = request.json['blog_id']
        user_id = request.json['user_id']
        upvote_info = {'blog_id': blog_id, 'user_id': user_id}
        if value == 1:
            if db.upvote.find_one(upvote_info) is None:
                db.upvote.insert_one(upvote_info)
                db.my_collection.update({"blog_id": blog_id}, {"$inc": {"upvote_count": 1}})  # this could be an error
                return 'Upvote registered'
            return 'Upvote already registered'
        elif value == -1:
            db.upvote.delete_one(upvote_info)
            db.my_collection.update({"blog_id": blog_id}, {"$inc": {"upvote_count": -1}})  # this could be an error
            return 'Upvote deleted'
        return 'Upvote not registered'
    return json.loads(json_util.dumps(db.upvote.find()))


@app.route("/upvote_count", methods=['POST', 'GET'])
@cross_origin()
def upvote_count():
    if request.method == "POST":
        blog_id = request.json['blog_id']
        count = db.upvote.count_documents({"blog_id": blog_id})
        return str(count)

    return "endpoint exists"
