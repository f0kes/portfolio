from flask import Flask, request, jsonify, render_template
import numpy as np
from search import load_md_files, search

app = Flask(__name__)

# Load documents and precompute embeddings on app startup
embedded_docs = load_md_files("./md_files")

# flask cors
from flask_cors import CORS

CORS(app)


def is_json_serializable(obj):
    try:
        jsonify(obj)  # Try serializing with the standard JSON library
        return True
    except (TypeError, OverflowError):
        return False


def clean_dict_for_jsonify(data):
    cleaned_dict = {}

    for key, value in data.items():
        # Check if value is JSON serializable
        if is_json_serializable(value):
            cleaned_dict[key] = value
        # Check if value is a NumPy object (number or array-like)
        elif isinstance(value, np.generic):  # Handles numpy scalar types
            cleaned_dict[key] = value.item()
        elif (
            isinstance(value, np.ndarray) and value.size == 1
        ):  # Handles 1-element numpy arrays
            cleaned_dict[key] = value.item()

    return cleaned_dict


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
    results = [
        {k: clean_dict_for_jsonify(v) for k, v in result.items()} for result in results
    ]
    return jsonify(results), 200


# Start the server
if __name__ == "__main__":
    app.run(debug=True)
