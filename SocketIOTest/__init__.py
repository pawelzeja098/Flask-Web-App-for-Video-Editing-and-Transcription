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
play = False



def capture_frames():
    """Capture frames from the default camera and emit them to clients."""
    # cap = cv2.VideoCapture(0)
    global cap,play
    # cap = get_frames_from_film(frame = 100)
    video_path = "E:/Programowanie/MOV2024.mp4"
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        if not play:
            eventlet.sleep(0.1)
            continue

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

@socketio.on("start")
def handle_start():
    print(" Command: START")
    global play
    play = True
    socketio.emit("status", {"message": "Streaming started"})  # Wysyłamy status do klienta

@socketio.on("stop")
def handle_stop():
    print(" Command: STOP")
    global play
    play = False
    socketio.emit("status", {"message": "Streaming stopped"})

@socketio.on("rewind")
def handle_rewind():
    print("Otrzymano komendę: REWIND")
    global cap
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    socketio.emit("status", {"message": "Rewinding video"})

# def get_frames_from_film(frame):
#     video_path = "E:/Programowanie/MOV2024.mp4"
#     video = cv2.VideoCapture(video_path)


