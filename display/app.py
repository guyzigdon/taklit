from flask import Flask, jsonify, render_template, request

from .client import GlobalData

data = GlobalData()


app = Flask(__name__)


@app.route("/")
def home():
    return render_template(
        "index.html"
    )  # Ensure the HTML file is in the 'templates' folder


@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(data.model_dump())


@app.route("/data", methods=["POST"])
def post_data():
    global data
    try:
        # Parse JSON data from the request
        json_data = request.json

        # Validate and parse JSON data using Pydantic
        data = GlobalData(**json_data)

        # Return the validated data as a JSON response
        return jsonify(data.model_dump()), 201

    except Exception as e:
        # Handle validation errors or other exceptions
        return jsonify({"error": str(e)}), 400
