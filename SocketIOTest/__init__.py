"""
The flask application package.
"""

# Import necessary libraries

from flask import Flask
from flask_socketio import SocketIO
from SocketIOTest.views import init_routes




def create_app():
# Initialize Flask application and Socket.IO
    app = Flask(__name__)
    socketio = SocketIO(app,cors_allowed_origins="*",async_mode='threading')
    # app.video_controller = VideoControler(cap,subtitles,video_length,fps)    
    
    init_routes(app, socketio)

    return app, socketio




