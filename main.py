from flask import Flask
from rout import user_blueprint, room_blueprint

app = Flask(__name__)

app.register_blueprint(user_blueprint)
app.register_blueprint(room_blueprint)

STUDENT_ID = 7


@app.route(f'/hello-world')
def hello_world():
    return f"Hello world!", 200


@app.route(f'/hello-world-{STUDENT_ID}')
def hello_world_student():
    return f"Hello world, {STUDENT_ID}!", 200


if __name__ == "__main__":
    app.run(debug=True)