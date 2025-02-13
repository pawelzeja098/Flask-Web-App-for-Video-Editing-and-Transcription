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
    global cap,play,speed, video_length
    # cap = get_frames_from_film(frame = 100)
    video_path = "E:/Programowanie/MOV2024.mp4"
    cap = cv2.VideoCapture(video_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  
    fps = cap.get(cv2.CAP_PROP_FPS)  
    video_length = total_frames / fps  
    # eventlet.sleep(0.0001)
    # socketio.emit("set_max_time", {"max_time": int(video_length)})

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        if not play:
            eventlet.sleep(0.1)
            continue

        ret, frame = cap.read()
        
        if not ret:
            # print("Error: Failed to capture frame.")
            play = False
            continue
            

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        # Emit the encoded frame to all connected clients
        asd = cap.get(cv2.CAP_PROP_POS_MSEC)
        curr_time = int(asd/1000)
        socketio.emit('frame', jpg_as_text)
        socketio.emit('curr_film_time', {"curr_time" : curr_time})
        eventlet.sleep(1/fps)

    cap.release()
    
import SocketIOTest.views

@socketio.on("start")
def handle_start():
    print(" Command: START")
    global play
    play = True
    socketio.emit("status", {"message": "Streaming started"})
    socketio.emit("set_max_time", {"max_time": int(video_length)})

@socketio.on("stop")
def handle_stop():
    print(" Command: STOP")
    global play
    play = False
    socketio.emit("status", {"message": "Streaming stopped"})


@socketio.on("rewind")
def handle_rewind(data):
    print("Command: REWIND")
    global cap
    time = int(data['time'])
    cap.set(cv2.CAP_PROP_POS_MSEC, time * 1000)
    
    socketio.emit("status", {"message": f"Rewinding video to {time}s"})



# def get_frames_from_film(frame):
#     video_path = "E:/Programowanie/MOV2024.mp4"
#     video = cv2.VideoCapture(video_path)


