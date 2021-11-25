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
    tasks = Task.query.all()
    return render_template("home.html", task_list=tasks)


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
def create_task():
    task_data = request.form
    db.session.add(
        Task(
            name=task_data.get("name"),
            body=task_data.get("body"),
            priority=int(task_data.get("priority"))
        )
    )
    db.session.commit()
    return redirect("/")


@app.get("/tasks/<int:pk>")
def get_single_task(pk):
    task = Task.query.filter_by(id=pk).first()
    return render_template("detail_view.html", task=task)


@app.get("/tasks/<int:pk>/delete")
def finish_task(pk):
    Task.query.filter_by(id=pk).delete()
    db.session.commit()
    return redirect("/")