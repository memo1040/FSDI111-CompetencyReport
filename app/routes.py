from flask import (
    Flask, 
    render_template,
    request,
    redirect
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
db = SQLAlchemy(app)

from app.database.task import Task

TLIST = []


@app.get("/")
def index():
    Task.query.all()
    return render_template("home.html")


@app.get("/about")
def about_me():
    me = {
        "first_name": "Guillermo",
        "last_name": "Monge",
        "bio": "Web Developer"
    }
    return render_template("about.html", user=me)


@app.get("/tasks/create")
def get_form():
    return render_template("create_task.html")


@app.post("/tasks")
def create_task(name, body, priority):
    db.session.add(
        Task(
            name=name,
            body=body,
            priority=priority
        )
    )
    db.session.commit()
    return redirect("/")