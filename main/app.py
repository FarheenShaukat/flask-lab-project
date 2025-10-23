from flask import Flask, jsonify, request, render_template
from jinja2 import TemplateNotFound

app = Flask(__name__)

# Store data temporarily (in-memory)
data_store = []


@app.route("/")
def home():
    """Homepage route - renders index.html or fallback"""
    try:
        return render_template("index.html")
    except TemplateNotFound:
        return "<h1>Flask Lab Project</h1><p>Welcome (template missing)</p>", 200


@app.route("/health")
def health():
    """Health check route"""
    return jsonify({
        'status': 'healthy',
        'message': 'Flask application is running successfully'
    }), 200


@app.route("/data", methods=["POST"])
def post_data():
    """POST endpoint - accept JSON payload and store it"""
    payload = request.get_json(silent=True)
    
    if not payload:
        return jsonify({
            "error": "Invalid or missing JSON payload"
        }), 400

    # Store the data
    data_store.append(payload)
    
    result = {
        "received": payload,
        "processed": True,
        "total_items": len(data_store)
    }
    return jsonify(result), 201


@app.route("/data", methods=["GET"])
def get_data():
    """GET endpoint - retrieve all stored data"""
    return jsonify({
        'status': 'success',
        'data': data_store,
        'count': len(data_store)
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)