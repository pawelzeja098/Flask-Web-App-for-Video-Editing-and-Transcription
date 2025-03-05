"""
This script runs the SocketIOTest application using a development server.
"""

from os import environ
from SocketIOTest import create_app

app, socketio = create_app()

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    
    # socketio.start_background_task(capture_frames)
    socketio.run(app, host='0.0.0.0', port=5000)
