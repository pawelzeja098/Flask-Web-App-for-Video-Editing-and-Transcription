import whisper
import numpy as np
from pydub import AudioSegment
import time
import csv
from moviepy import VideoFileClip


class TranscriptionController:
    def __init__(self,video_path) -> None:
        self.video_path = video_path

    def get_audio_from_video(self,video_path):
        """
        Get audio from video to transcribe.
        Parameters:
        video_path 
        """
        video = VideoFileClip(video_path)
        # Load the mp3 file
        audio = video.audio
        audio_file_path = "extracted_audio.wav"
        audio.write_audiofile(audio_file_path)
        video.close()
        audio = AudioSegment.from_file(audio_file_path)

        trimmed_audio = audio

        # cut_audio = False

        # if cut_audio:

        #     start_time = 73 * 1000   
        #     end_time = 103 * 1000    

        #     # Trim the audio
        #     trimmed_audio = audio[start_time:end_time]

        trimmed_audio = trimmed_audio.set_frame_rate(16000).set_channels(1)


    # Convert to numpy array and normalize audio data to be between -1.0 and 1.0
        audio = np.array(trimmed_audio.get_array_of_samples()).astype(np.float32) / 32768.0

        return audio

    def transcribe(self,audio,word_by_word = False,model = "large"):
        """
        Trascribe audio using whisper

        Parameters:
        audio
        word_by_word - bool If you want to get every said word time
        model - whisper model by deafult large
        """
    
        model = whisper.load_model("large")
    

    
    
        start = time.time()
        result = model.transcribe(audio,word_timestamps=word_by_word)
        stop = time.time()

        time_transcribe = stop - start
        print(f"Czas: {time_transcribe}")



        return result, word_by_word

    def convert_to_csv(self,result,word_by_word):

        """
        Convert result to csv file

        Parameters:
        result from model
        word_by_word - bool If you want to get every said word time
        """

        if word_by_word:
            with open("transcription.csv", "w", newline="", encoding="utf-8") as csvfile:
                csvwriter = csv.writer(csvfile)
            
                csvwriter.writerow(["word", "start", "stop"])
                for segment in result["segments"]:
                    for word_info in segment["words"]:
                        word = word_info["word"]
                        start = word_info["start"]
                        end = word_info["end"]
                        csvwriter.writerow([word, f"{start:.2f}", f"{end:.2f}"])
        else:
            with open("transcription.csv", "w",newline = "", encoding="utf-8") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(["text", "start", "stop"])
                for segment in result["segments"]:  
                    text = segment["text"]         
                    start = segment["start"]       
                    stop = segment["end"]          
                
                    csvwriter.writerow([text, f"{start:.2f}", f"{stop:.2f}"])

