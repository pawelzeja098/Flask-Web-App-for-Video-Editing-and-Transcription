import cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class VideoControler:
    def __init__(self,cap,subtitles,video_length,fps) -> None:
        self.cap = cap
        self.subtitles = subtitles
        self.play = False
        self.video_length = video_length
        self.fps = fps
        self.trim_start_value = 0
        self.trim_stop_value = 0

    def handle_rewind(self,time):
   
        self.subtitles.search_for_sub_idx(time)
        self.cap.set(cv2.CAP_PROP_POS_MSEC, time * 1000)

    def handle_start_stop(self,play):
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

        font = ImageFont.truetype(font_path, 40)  
        position = (50, img.shape[0] - 50)  
        color = (255, 0, 0)  

        draw.text(position, text, font=font, fill=color)  

        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    def trim_video(self):
        
        output_folder = 'E:/Programowanie/TrimmedVideos'
        output_file = 'trimmedvideo.mp4'

        

        

        cap_trim = cv2.VideoCapture("E:/Programowanie/MOV2024.mp4")

        cap_trim.set(cv2.CAP_PROP_POS_MSEC, self.trim_start_value * 1000)

        w = int(cap_trim.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap_trim.get(cv2.CAP_PROP_FRAME_HEIGHT))

        result_video = cv2.VideoWriter(os.path.join(output_folder, output_file), cv2.VideoWriter_fourcc(*"mp4v"), self.fps, (w, h))
        
        # skip_frames = 200

        # for _ in range(skip_frames):

            
        #     ret, frame = cap_trim.read()
        curr_time = cap_trim.get(cv2.CAP_PROP_POS_MSEC) / 1000
        
        text_time_start = self.subtitles.search_for_sub_idx(self.trim_start_value)

        while curr_time < self.trim_stop_value:

            ret, frame = cap_trim.read()

            if ret:



                if curr_time > self.subtitles.text_times[text_time_start][0]:
            
                    frame = self.put_text_on_image(frame,self.subtitles.text[text_time_start]['text'])
                    if curr_time > self.subtitles.text_times[text_time_start][1]:
                        text_time_start += 1
            

                result_video.write(frame)


                curr_time = cap_trim.get(cv2.CAP_PROP_POS_MSEC) / 1000

        cap_trim.release()


