from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

# Database and collection
db = client.todo_db
todos = db.todos


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form["content"]
        degree = request.form["degree"]
        todos.insert_one({
            "content": content,
            "degree": degree
        })
        return redirect(url_for("index"))
    
    all_docs = todos.find()
    return render_template("index.html", todos=all_docs)


@app.route("/<id>/delete", methods=["POST"])
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("index"))


def handler(event, context):  # For Vercel Serverless
    return app(event, context)
