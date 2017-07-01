import os

from flask import Flask, jsonify, send_from_directory, request, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#import pwapi.secret as secret

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://%s:%s@%s/%s" % (
    # ARGS.dbuser, ARGS.dbpass, ARGS.dbhost, ARGS.dbname
    os.environ["DBUSER"], os.environ["DBPASS"], os.environ["DBHOST"], os.environ["DBNAME"]
)

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

from models import *

@app.route("/")
def root():
    data = {"hello": "world"}
    return jsonify(data)

@app.route("/posts")
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)

# Public Directory:
@app.route("/<path:path>", strict_slashes=False)
def send_static(path):
  return send_from_directory("public", path)
