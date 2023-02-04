from flask import Flask, jsonify, request

from model import setup_db, Todo


def create_app():
    app = Flask(__name__)
    setup_db(app)
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
    return jsonify([todo.to_dict() for todo in todos])


@app.route("/<int:todo_id>", methods=[GET])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    return (todo.to_dict(), 200) if todo else ("Not found", 404)


@app.route("/", methods=[POST])
@validate(fields=["title", "description"])
def add_todo():
    data: dict = request.get_json()
    todo = Todo(title=data.get("title"), description=data.get("description"))
    todo.save()
    return index()


@app.route("/<int:todo_id>", methods=[PATCH])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return "Not Found", 404
    data: dict = request.get_json()
    todo.title = data.get("title", todo.title)
    todo.desc = data.get("description", todo.desc)
    todo.update()
    return index()


@app.route("/<int:todo_id>", methods=[DELETE])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return "Not Found", 404
    todo.delete()
    return index()


if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")
