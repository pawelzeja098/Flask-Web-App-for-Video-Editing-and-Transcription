import csv

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
        if time < self.text_times[0][0]:
            self.time_idx = i
            return
        for i in range(len(self.text_times) - 1):
            
            if time > self.text_times[i][0]:
                if time < self.text_times[i + 1][0]:  
                    self.time_idx = i
                    return
            i+=1

    def get_trimmed_subtitles(self,start,stop):
        i = 0
        trimmed_subtitles = []
        ts =''
        start_idx = 0
        stop_idx = 0
        

        if start < self.text_times[0][0]:
            start_idx = 0
        
        for i in range(len(self.text_times) - 1):
            
            if start > self.text_times[i][0]:
                if start < self.text_times[i + 1][0]:  
                    start_idx = i
                    
            i+=1
        i = 0
        for i in range(len(self.text_times) - 1):
            
            if stop > self.text_times[i][0]:
                if stop < self.text_times[i + 1][0]:  
                    stop_idx = i
                    
            i+=1

        for i in range(start_idx,stop_idx + 1):

            trimmed_subtitles.append(self.text[i]['text'])
            ts += self.text[i]['text'] + ' '
        return ts
