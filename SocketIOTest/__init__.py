﻿"""
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

# Initialize Flask application and Socket.IO
app = Flask(__name__)
socketio = SocketIO(app)
play = False



# class Subtitles():
#     def __init__(self) -> None:

class Subtitles:
    def __init__(self,text,text_times) -> None:
        self.text = text
        self.text_times = text_times
        self.time_idx = 0

    @staticmethod
    def capture_subtitles_csv(filename ='E:/Programowanie/transcription.csv'):
        text = []
        text_times = []
        with open(filename,'r',encoding='utf-8') as csv_file:
            csvreader = csv.DictReader(csv_file)
            for row in csvreader:
                text.append({
                    "text" : row["Sentence"]
                    })
                text_times.append((float(row["Start"]),float(row["Stop"])))
        subtitles = Subtitles(text = text, text_times = text_times)
        return subtitles
        

    def search_for_sub_idx(self,time):
        """
        Searching for subtitles index after rewinding film
        """
        i = 0

        for i in range(len(self.text_times) - 1):
            if time > self.text_times[i][0]:
                if time < self.text_times[i + 1][0]:  
                    self.time_idx = i
                    
            i+=1

class VideoControler:
    def __init__(self,cap,subtitles,video_length,fps) -> None:
        self.cap = cap
        self.subtitles = subtitles
        self.play = False
        self.video_length = video_length
        self.fps = fps

    def handle_rewind(self,time):
   
        self.subtitles.search_for_sub_idx(time)
        self.cap.set(cv2.CAP_PROP_POS_MSEC, time * 1000)

    def handle_start_stop(self,play):
        self.play = play
   
    
cap = cv2.VideoCapture("E:/Programowanie/MOV2024.mp4")
subtitles = Subtitles.capture_subtitles_csv()
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  
fps = cap.get(cv2.CAP_PROP_FPS)  
video_length = total_frames / fps

app.video_controller = VideoControler(cap,subtitles,video_length,fps)        

# def capture_subtitles():
#     """
#     Get subtitles text and times from csv file
#     """

#     global text_times
#     subtitles = []
#     text_times = []
#     with open('E:/Programowanie/transcription.csv','r',encoding='utf-8') as csv_file:
#         csvreader = csv.DictReader(csv_file)
#         for row in csvreader:
#             subtitles.append({
#                 "text" : row["Sentence"],
#                 "start" : float(row["Start"]),
#                 "stop" : float(row["Stop"])
#                 })
#             text_times.append((float(row["Start"]),float(row["Stop"])))
            
#     return subtitles, text_times
    
    



def put_text_on_image(img,text):
    """
    Putting text on frame
    """

    font = cv2.FONT_HERSHEY_SIMPLEX

    # org
    img_height, img_width, _ = img.shape
    org = (50, img_height - 50)

    # fontScale
    fontScale = 1
 
    # Blue color in BGR
    color = (255, 0, 0)

    # Line thickness of 2 px
    thickness = 2

    img = cv2.putText(img,text, org, font, fontScale, 
                 color, thickness, cv2.LINE_AA, False)

    return img

# def search_for_sub_idx(time):
#     """
#     Searching for subtitles index after rewinding film
#     """
#     i = 0
#     global cap, time_idx
#     for i in range(len(text_times) - 1):
#         if time > text_times[i][0]:
#             if time < text_times[i + 1][0]:  
#                 time_idx = i
#                 return time_idx

#         i+=1

def capture_frames():
    """Capture frames from the default camera and emit them to clients."""
    # cap = cv2.VideoCapture(0)
    
    # cap = get_frames_from_film(frame = 100)
    # video_path = "E:/Programowanie/MOV2024.mp4"
    # cap = cv2.VideoCapture(video_path)

    cap = app.video_controller.cap


    # subtitles, text_time = capture_subtitles()
    subtitles = app.video_controller.subtitles
    
    # sub_idx = 0
    # time_idx = 0



    # total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  
    # fps = cap.get(cv2.CAP_PROP_FPS)  
    # video_length = total_frames / fps  
    # eventlet.sleep(0.0001)
    # socketio.emit("set_max_time", {"max_time": int(video_length)})

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # text_time = subtitles[0]['start']
    while True:
        if not app.video_controller.play:
            eventlet.sleep(0.1)
            continue

        ret, frame = cap.read()
        curr_time = cap.get(cv2.CAP_PROP_POS_MSEC)
        
        

        if not ret:
            # print("Error: Failed to capture frame.")
            app.video_controller.play = False
            continue
       

        if curr_time/1000 > subtitles.text_times[subtitles.time_idx][0]:
            
            frame = put_text_on_image(frame,subtitles.text[subtitles.time_idx]['text'])
            if curr_time/1000 > subtitles.text_times[subtitles.time_idx][1]:
                subtitles.time_idx += 1


        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        # Emit the encoded frame to all connected clients
        
        curr_time_s = int(curr_time/1000)
        socketio.emit('frame', jpg_as_text)
        socketio.emit('curr_film_time', {"curr_time" : curr_time_s})
        eventlet.sleep(1 / (app.video_controller.fps * 1.5))
        

    cap.release()
    
import SocketIOTest.views



@socketio.on("start")
def handle_start():
    print(" Command: START")
    app.video_controller.handle_start_stop(play=True)
    socketio.emit("status", {"message": "Streaming started"})
    socketio.emit("set_max_time", {"max_time": int(app.video_controller.video_length)})

@socketio.on("stop")
def handle_stop():
    print(" Command: STOP")
    app.video_controller.handle_start_stop(play=False)
    socketio.emit("status", {"message": "Streaming stopped"})


@socketio.on("rewind")
def handle_rewind(data):
    print("Command: REWIND")
    global cap, time_idx, subtitles
    time = int(data['time'])
    
    app.video_controller.handle_rewind(time)
    # app.video_controller.subtitles.search_for_sub_idx(time)
    
    # app.video_controller.cap.set(cv2.CAP_PROP_POS_MSEC, time * 1000)
   
    
    socketio.emit("status", {"message": f"Rewinding video to {time}s"})



# def get_frames_from_film(frame):
#     video_path = "E:/Programowanie/MOV2024.mp4"
#     video = cv2.VideoCapture(video_path)


