from flask import Flask

app = Flask(__name__)


STUDENT_ID = 7


@app.route(f'/hello-world')
def hello_world():
    return f"Hello world!", 200


@app.route(f'/hello-world-{STUDENT_ID}')
def hello_world_student():
    return f"Hello world, {STUDENT_ID}!", 200


if __name__ == "__main__":
    app.run(debug=True)