from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    print("Received data:", data)  # prints to console where API is running
    return jsonify({"status": "ok", "received": data}), 200
    if __name__ == "__main__":
        app.run(port=5000, debug=True)
