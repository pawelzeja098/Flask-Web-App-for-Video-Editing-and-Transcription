"""
The flask application package.
"""

# from flask import Flask
# app = Flask(__name__)



# Import necessary libraries
import cv2
import base64
import eventlet
from flask import Flask, render_template
from flask_socketio import SocketIO

# Initialize Flask application and Socket.IO
app = Flask(__name__)
socketio = SocketIO(app)




def capture_frames():
    """Capture frames from the default camera and emit them to clients."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        # Emit the encoded frame to all connected clients
        socketio.emit('frame', jpg_as_text)

        eventlet.sleep(0.1)

    cap.release()
    
import SocketIOTest.views
