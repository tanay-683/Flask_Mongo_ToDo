from flask import Flask, render_template, url_for, request, redirect
from bson.objectid import ObjectId
# from models import todos
from pymongo import MongoClient

app = Flask(__name__)


# # Initialize MongoDB client
client = MongoClient('localhost', 27017)

# Database and collection setup
db = client.todo_db
todos = db.todos


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
    app.run(debug=True, host='0.0.0.0', port=5000)