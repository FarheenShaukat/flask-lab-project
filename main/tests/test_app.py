from flask import Flask, jsonify, request, render_template
from jinja2 import TemplateNotFound

app = Flask(__name__)


@app.route("/")
def home():
    # Try to render the template; if it's missing (test environments) return a simple HTML fallback
    try:
        return render_template("index.html")
    except TemplateNotFound:
        return "<h1>Flask Lab Project</h1><p>Welcome (template missing)</p>", 200


@app.route("/health")
def health():
    return "OK", 200


@app.route("/data", methods=["POST"])
def data():
    # Accept JSON payload and echo back with a simple transformation
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    # Simple processing: add a processed flag
    result = {"received": payload, "processed": True}
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)