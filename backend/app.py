from flask import Flask, request, jsonify, render_template
import numpy as np
from search import load_md_files, search

app = Flask(__name__)

# Load documents and precompute embeddings on app startup
embedded_docs = load_md_files("./md_files")

# flask cors
from flask_cors import CORS

CORS(app)


# Custom function to convert NumPy types to Python native types
def convert_numpy(obj):
    if isinstance(obj, np.generic):
        return (
            obj.item()
        )  # Convert NumPy scalar (e.g., np.float32) to native Python type
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


# Home route to render the search interface (serves index.html)
@app.route("/")
def index():
    return render_template("index.html")


# API route to perform the search
@app.route("/search", methods=["POST"])
def search_documents():
    data = request.json
    query = data.get("query", "")
    threshold = float(data.get("threshold", 0.7))  # Default threshold = 0.7

    if not query:
        return jsonify({"error": "Query is missing!"}), 400

    # Perform the search with a similarity threshold
    results = search(query, embedded_docs)

    if not results:
        return jsonify({"message": "No relevant documents found."})

    # Use custom conversion for NumPy types before returning the response
    return jsonify(results), 200


# Start the server
if __name__ == "__main__":
    app.run(debug=True)
