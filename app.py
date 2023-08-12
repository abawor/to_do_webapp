from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_migrate import Migrate


app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'axiu'
app.config['BASIC_AUTH_PASSWORD'] = '1437'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
basic_auth = BasicAuth(app)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    # show all todos
    todo_list = ToDo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)


@app.route("/add", methods=["POST"])
@basic_auth.required
def add():
    # add new item
    title = request.form.get("title")
    new_todo = ToDo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/update/<int:todo_id>")
@basic_auth.required
def update(todo_id):
    # set existing item to complete/not complete
    todo = ToDo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>")
@basic_auth.required
def delete(todo_id):
    # delete existing item
    todo = ToDo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))
