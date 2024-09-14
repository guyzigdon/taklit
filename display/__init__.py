import multiprocessing.process
import threading
import multiprocessing

from .app import app

PORT = 5000

def run_html():
    import webview
    # Open the webview window on the specified display
    webview.create_window("HTML Display", f"http://localhost:5000", fullscreen=True)
    webview.start()

def start_display_server():
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=PORT)).start()

# # Function to start the Flask server
# def start_server():
#     # Start the Flask server in a separate thread
#     threading.Thread(target=lambda: ).start()
#     # multiprocessing.Process(target=run_html).start()
