"""
The flask application package.
"""

# from flask import Flask
# app = Flask(__name__)



# Import necessary libraries
import time
import cv2
import base64
import eventlet
import csv
from flask import Flask, render_template
from flask_socketio import SocketIO
from SocketIOTest.views import init_routes
from SocketIOTest.SubtitlesClass import Subtitles
from SocketIOTest.VideoControlerClass import VideoControler



def create_app():
# Initialize Flask application and Socket.IO
    app = Flask(__name__)
    socketio = SocketIO(app,cors_allowed_origins="*",async_mode='threading')
    play = False

    cap = cv2.VideoCapture("E:/Programowanie/MOV2024.mp4")
    subtitles = Subtitles.capture_subtitles_csv()
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  
    fps = cap.get(cv2.CAP_PROP_FPS)  
    video_length = total_frames / fps

    # app.video_controller = VideoControler(cap,subtitles,video_length,fps)    
    
    init_routes(app, socketio)

    return app, socketio




