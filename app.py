from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def root():
    data = {"hello": "world"}
    return jsonify(data)

# Public Directory:
@app.route("/<path:path>", strict_slashes=False)
def send_static(path):
  return send_from_directory("public", path)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
