import threading, os, re
from extract.youtube.youtube_videos import VideoAPI
from extract.structures.YTFrame import YTFrame
from config import base_dir, storage_json


class YoutubeScanner(threading.Thread):
    def __init__(self, channleId, period=48):
        threading.Thread.__init__(self)
        self.channel = channleId
        self.hours = period

    def run(self):
        while True:
            pass


class IdTranslator(VideoAPI):
    def __init__(self):
        VideoAPI.__init__()
        self.dictionary_path = os.path.join(base_dir, storage_json)
        os.makedirs(self.dictionary_path, exist_ok=True)

    def __init_dict(self):
        files = os.listdir(path=self.dictionary_path)
        #  files = os.scandir(path=self.dictionary_path)
        acc_re = f"@.*\."
        for file in files:
            idx = re.search(acc_re, file).group().strip("@.")
            thread = threading.Thread(target=None)

