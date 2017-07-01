from flask import Flask, jsonify, send_from_directory
app = Flask(__name__)
#import pwapi.app as app
from flask_sqlalchemy import SQLAlchemy
import pwapi.secret as secret
#from models import db

app.config['DEBUG'] = secret.DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = secret.DATABASE_URI

db = SQLAlchemy()
db.init_app(app)

@app.route("/")
def root():
    data = {"hello": "world"}
    return jsonify(data)

# Public Directory:
@app.route("/<path:path>", strict_slashes=False)
def send_static(path):
  return send_from_directory("public", path)

#if __name__ == "__main__":
app.run(debug=True, host="0.0.0.0")
