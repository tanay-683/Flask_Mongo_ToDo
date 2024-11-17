from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# ==================================
# initializing mongo client
client = MongoClient('localhost', 27017)

# creating a db
db = client.todo_db

# creating a collection
todos = db.todos

# ==================================

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == 'POST':
        content = request.form["content"]
        degree = request.form["degree"]
        todos.insert_one({
            "content" : content,
            "degree" : degree
        })
        # redirecting again to home page after user clicks submit
        return redirect(url_for("index"))
    
    # getting all the todos
    all_docs = todos.find()
    
    # sending all_docs as a variable through jinja
    return render_template("index.html", todos = all_docs)

# ==================================

@app.post("/<id>/delete") # this is equal to @app.route("/", methods=["POST"])
def delete(id):
    todos.delete_one({"_id":ObjectId(id)})
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True,host='127.0.0.1', port=5000)
