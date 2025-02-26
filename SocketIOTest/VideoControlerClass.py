import cv2

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
