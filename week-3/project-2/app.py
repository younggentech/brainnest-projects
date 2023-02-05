from flask import Flask, jsonify, request
from flask_cors import CORS
from model import setup_db, Todo


def create_app():
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    return app


app = create_app()
GET, POST, PATCH, DELETE = "GET", "POST", "PATCH", "DELETE"


def validate(fields):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data: dict = request.get_json()
            missing_fields = list(set(fields).difference(set(data.keys())))
            if missing_fields:
                return f"missing: {', '.join([field for field in missing_fields])}.", 403
            return func(*args, **kwargs)

        return wrapper

    return decorator


@app.route("/", methods=[GET])
def index():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos]), 200


@app.route("/<int:todo_id>", methods=[GET])
def get_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    return todo


@app.route("/", methods=[POST])
@validate(fields=["title", "description"])
def add_todo():
    data: dict = request.get_json()
    todo = Todo(title=data.get("title"), description=data.get("description"))
    todo.save()
    return "Todo Saved Successfully.", 201


@app.route("/<int:todo_id>", methods=[PATCH])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data: dict = request.get_json()
    todo.title = data.get("title", todo.title)
    todo.desc = data.get("description", todo.desc)
    todo.completed = data.get("completed", todo.completed)
    todo.update()
    return "Todo Updated Successfully.", 200


@app.route("/<int:todo_id>", methods=[DELETE])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.delete()
    return "Todo Deleted Successfully.", 200


@app.errorhandler(404)
def not_found(error):
    return jsonify("Not Found"), 404


@app.errorhandler(400)
def not_found(error):
    return jsonify("Bad Request"), 400


# TODO: add change the completion of a todo.
if __name__ == '__main__':
    app.run(port=5050, host="0.0.0.0")
