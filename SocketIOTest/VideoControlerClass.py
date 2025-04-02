import os.path
import cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from SocketIOTest.SubtitlesClass import Subtitles
import moviepy as mp
import threading
import eventlet
import base64
import time
import tempfile

class VideoControler:

    @property
    def  CurrentTime(self,_time):
        """The price property."""
        return self._currentTime

    @CurrentTime.setter
    def CurrentTime(self, value):
        """   """
        with self.lock_cap:
            self.cap.set(cv2.CAP_PROP_POS_MSEC, value * 1000)
        self._currentTime = value

    def __init__(self,filepath,socketio) -> None:
        self.name = filepath
        self.socketio = socketio
        self.filepath = filepath


        self.cap = cv2.VideoCapture(filepath)
        filepath_csv = filepath.replace(".mp4", ".csv")
        self.subtitles = Subtitles.capture_subtitles_csv(filepath_csv)
        self.play = False
        
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))  
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)  
        self.video_length = total_frames / self.fps
        
        self.trim_start_value = 0
        self.trim_stop_value = 0

        self.lock_cap = threading.Lock()

        self._stop_event = threading.Event()

        self.running = True


        self.thread = threading.Thread(target=self.capture_frames)

        #automatic kill thread
        self.thread.daemon = True

        self.thread.start()


    def handle_rewind(self,time):
   
        self.subtitles.search_for_sub_idx(time)
        self.cap.release()
        self.cap = cv2.VideoCapture(self.filepath)
        self.cap.set(cv2.CAP_PROP_POS_MSEC, time * 1000)
        self.handle_start_stop(True)

    def handle_start_stop(self,play):
        self.socketio.emit("status", {"message": "Streaming started"})
        self.socketio.emit("set_max_time", {"max_time": int(self.video_length)})
        self.play = play
    

    def put_text_on_image(self,img,text):
        """
        Putting text on frame
        """
        # ft2 = cv2.freetype.createFreeType2()
        # font = "arial.ttf"

        # # org
        # img_height, img_width, _ = img.shape
        # org = (50, img_height - 50)

        # # fontScale
        # fontScale = 1
 
        # # Blue color in BGR
        # color = (255, 0, 0)

        # # Line thickness of 2 px
        # thickness = 2

        # img = cv2.putText(img,ft2, org, font, fontScale, 
        #              color, thickness, cv2.LINE_AA, False)

        # return img

        font_path="arial.ttf"
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  
        draw = ImageDraw.Draw(img_pil)

        font = ImageFont.truetype(font_path, 50)  
        position = (50, img.shape[0] - 50)  
        color = (255, 0, 0)  

        draw.text(position, text, font=font, fill=color)  

        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    def trim_video(self):
        filename = os.path.basename(self.filepath) 
        output_folder = 'E:/Programowanie/TrimmedVideos'
        output_file = os.path.join(output_folder, f"trimmed_{filename}") 

        
        print()
        

        cap_trim = cv2.VideoCapture(self.filepath)
        

        cap_trim.set(cv2.CAP_PROP_POS_MSEC, self.trim_start_value * 1000)

        w = int(cap_trim.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap_trim.get(cv2.CAP_PROP_FRAME_HEIGHT))

        result_video = cv2.VideoWriter(os.path.join(output_folder, output_file), cv2.VideoWriter_fourcc(*"XVID"), self.fps, (w, h))
        
        # skip_frames = 200

        # for _ in range(skip_frames):

            
        #     ret, frame = cap_trim.read()
        curr_time = cap_trim.get(cv2.CAP_PROP_POS_MSEC) / 1000
        
        text_time_start = self.subtitles.search_for_sub_idx(self.trim_start_value)

        trim_range = self.trim_stop_value - self.trim_start_value
        while curr_time < self.trim_stop_value:
 
            
            if self.running == False:
                break


            ret, frame = cap_trim.read()

            if ret:


                try:
                    if curr_time > self.subtitles.text_times[text_time_start][0]:
            
                        frame = self.put_text_on_image(frame,self.subtitles.text[text_time_start]['text'])
                        if curr_time > self.subtitles.text_times[text_time_start][1]:
                            text_time_start += 1
                except:
                    print("Error catching subtitles")

                result_video.write(frame)

                progress = (((curr_time - self.trim_start_value) / trim_range)) * 100;



                self.socketio.emit("progress_update",{"progress" :int(progress)})

                curr_time = cap_trim.get(cv2.CAP_PROP_POS_MSEC) / 1000

        result_video.release()
        cap_trim.release()
        
        audio = mp.AudioFileClip(self.filepath).subclipped(self.trim_start_value,self.trim_stop_value)
        video = mp.VideoFileClip(os.path.join(output_folder, output_file))
        # output_file = os.path.join("trimmed_", filename)
        mp_audio = mp.CompositeAudioClip([audio])
        video.audio = mp_audio
        

        video.write_videofile(os.path.join(output_folder, f"trimmed_with_audio{filename}"))

        self.socketio.emit("progress_update",{"progress" : 'Done'})



    def capture_frames(self):
        """Capture frames from the default camera and emit them to clients."""
        

        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            return

        # text_time = subtitles[0]['start']
        while True:
            if not self.play:
                eventlet.sleep(0.1)
                continue

            starttime=time.time()

            with self.lock_cap:
                ret, frame = self.cap.read()
                curr_time = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        
        

            if not ret:
                # print("Error: Failed to capture frame.")
                self.play = False
                continue
       
            try:
                if curr_time/1000 > self.subtitles.text_times[self.subtitles.time_idx][0]:
            
                    frame = self.put_text_on_image(frame,self.subtitles.text[self.subtitles.time_idx]['text'])
                    if curr_time/1000 > self.subtitles.text_times[self.subtitles.time_idx][1]:
                        self.subtitles.time_idx += 1
            except:
                print("Error catching subtitles")

            # Encode the frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')

            # Emit the encoded frame to all connected clients
        
            curr_time_s = int(curr_time/1000)
            self.socketio.emit('frame', jpg_as_text)
            self.socketio.emit('curr_film_time', {"curr_time" : curr_time_s})
            eventlet.sleep(1 / (self.fps * 1.5) - (time.time()-starttime))
            
            starttime=time.time()
        self.cap.set(cv2.CAP_PROP_POS_MSEC, 0)

        self.handle_start_stop(False)

        # self.cap.release()

    def stop_thread(self):
        self._stop_event.set()
        

        self.cap.release()