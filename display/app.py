from flask import Flask, jsonify, render_template, request
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

clients = []


@app.route("/")
def home():
    return render_template(
        "index.html"
    )  # Ensure the HTML file is in the 'templates' folder


# WebSocket route for clients
@sock.route("/ws")
def websocket(ws):
    global clients
    clients.append(ws)  # Add new client connection to the list
    while True:
        message = ws.receive()  # Keep the connection open to receive messages
        if not message:
            break  # Exit if the connection is closed
    clients.remove(ws)  # Remove client from the list when connection closes


@app.route("/data", methods=["POST"])
def post_data():
    global clients
    try:
        # Parse JSON data from the request
        json_data = request.data.decode("utf-8")

        # Send message to all connected WebSocket clients
        for client in clients:
            client.send(json_data)

        # Return the validated data as a JSON response
        return jsonify(json_data), 201

    except Exception as e:
        print(e)
        # Handle validation errors or other exceptions
        return jsonify({"error": str(e)}), 400
