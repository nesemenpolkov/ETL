from extract.youtube.youtube_comments import CommentAPI
from extract.youtube.youtube_videos import VideoAPI
from extract.structures.YTFrame import YTFrame
import threading, logging, time
from common.utils import elapse_time, time_delta, convert_time, check_response, jsonyfier, from_url
from config import logfile
from bs4 import BeautifulSoup
from common.templates import VIDEO_STATS

logging.basicConfig(filename=logfile, level=logging.DEBUG)
log = logging.getLogger(__name__)


class Downloader(threading.Thread):
    def __init__(self, name, id, object):  # queue -> of API keys
        threading.Thread.__init__()
        self.name = name
        self.id = id
        self.object = object
        print(f"[DAEMON-INFO]:Thread {self.name} started at {elapse_time()} for {self.id}...")

    def run(self):
        stime = elapse_time()
        while time_delta(hours=48) >= elapse_time() - stime:
            self.object.collectorman(self.id)  # <-- VideoAPI method
            print(
                f"[DAEMON-INFO]:{str(elapse_time())} Extraction successfully complited on thread {self.name} for video {self.id}...")
            time.sleep(3600)


class Extractor:
    def __init__(self, service="youtube", api_key=None, ):
        self.API_KEY = api_key
        self.service = service
        self.video = VideoAPI(API_KEY=self.API_KEY)
        self.comment = CommentAPI(API_KEY=self.API_KEY)

        self.settings = {
            "key": self.API_KEY,
            "fileFormat": "csv",
            "mode": "default",
            "id": None,
            "contentType": "video"
        }

    def settings(self, **kwargs):
        for key in kwargs.keys():
            if key not in ["key", "fileFormat", "mode", "id", "contentType"]:
                return f"Invalid argument {key}!"
        self.settings.update(kwargs)

    def setMode(self, mode="default"):
        self.settings.update({"mode": mode})

    def video_stat(self, object_id=None, object_type="channel",
                   format="csv",
                   filter=None):
        #  initing start parameters
        print(f"Starting extraction from: {object_type} {object_id}")
        result = None
        if not object_id and not self.settings["id"]:
            print("No source id, try again!")
            return False
        elif not self.settings["id"]:
            self.settings["id"] = object_id
        else:
            object_id = self.settings["id"]
        if object_type == "channel":
            print("channel")
            result = self.video.get_channel_videos(channelId=object_id)

        if object_type == "video":
            result = self.video.from_video(videoId=object_id)

        if format == "csv":
            try:
                print("trying to save")
                importance = self.settings["sourceImportance"]
                result.to_csv(sourceImportance=importance)
                print("Success!")
            except OSError as e:
                print(e)
                return False
        if format == "json":
            try:
                importance = self.settings["sourceImportance"]
                result.to_json(sourceImportance=importance)
            except OSError as e:
                print(e)
                return False

    def get_comments(self, object_id=None,
                     format="csv",
                     filter=None):
        if not object_id and not self.settings["id"]:
            print("No source id, try again!")
            return False
        elif not self.settings["id"]:
            self.settings["id"] = object_id
        else:
            object_id = self.settings["id"]

        result = self.comment.get_video_comments(videoId=object_id)

        if format == "csv":
            try:
                importance = self.settings["sourceImportance"]
                result.to_csv(sourceImportance=importance)
                print("Success!")
            except OSError as e:
                print(e)
                return False
        if format == "json":
            try:
                importance = self.settings["sourceImportance"]
                result.to_json(sourceImportance=importance)
            except OSError as e:
                print(e)
                return False

    def get_channel_id(self, channelName=None):
        if channelName:
            result = self.video.get_id(username=channelName)
            return result
        else:
            return f"Invalid input! Username cannot be -> {channelName}."

    def __init_channels_list(self, channels):
        if type(channels) != type([]):
            raise Exception(f"Wrong type. {type(channels)} is not supported!")
        self.settings.update({"id": channels})
        self.channels = channels
        for i in range(len(self.channels)):
            channel = self.channels[i]
            stime = elapse_time()
            self.channels[i] = (stime, channel)
        print(f"[INFO]:{str(elapse_time)} Channels {len(self.channels)} initialized.....")

    def monitor(self, channels=list(), interval=600, duration=48, delta=900, isInfinite=False):
        self.__init_channels_list(channels)
        if isInfinite:
            duration = 9999999999999
        self.settings.update({
            "fileForamt": "csv",
            "contentType": "video",
            "timeInterval": interval,
            "timeDelta": delta,
            "duration": duration
        })

    def __thread_maker(self):
        print(f"[INFO]:{str(elapse_time)} Scanning procedure started...")
        count = 0
        while 1:
            for i in range(len(self.channels)):
                video = VideoAPI(API_KEY=self.API_KEY).activities(channelId=self.channels[i][1], isMonitor=True)
                if video:
                    new_thread = Downloader(name=str(count), id=video)
                    new_thread.setDaemon(True)
                    new_thread.start()
                    stime = elapse_time()
                    self.channels[i][0] = stime
                    count += 1
                else:
                    print(f"Channel {self.channels[i][1]} is checked...")
            time.sleep(self.settings["timeInterval"])

    def run(self, isBackground=False):

        if isBackground:
            try:
                m_thread = threading.Thread(target=self.__thread_maker)
                m_thread.setDaemon(True)
                m_thread.start()
                m_thread.join()
            except Exception as e:
                log.error(e)
        else:
            self.__thread_maker()
        #  ___________________________________
        #  place for additional code
        #  ___________________________________
        #  last thing in this method
        if isBackground:
            # m_thread.join()
            pass

    def get_activity(self, channelId, isMonitor=False):
        x = self.video.activities(channelId=channelId, isMonitor=isMonitor)
        print(x)


if __name__ == "__main__":
    test = Extractor(service="youtube", api_key="AIzaSyD49bsFeWc_Nvx-r5wuPy7RkPuiCFQN46E")
    test_sample = ["UC84J-P1AEat5jPz7C1vKhsw", "UC_IEcnNeHc_bwd92Ber-lew", "UCKonxxVHzDl55V7a9n_Nlgg",
                   "UCFU30dGHNhZ-hkh0R10LhLw", "UCsA_vkmuyIRlYYXeJueyIJQ", "UCdIEDjRlFiBdfQ0hqdSWHZw",
                   "UCQ4YOFsXjG9eXWZ6uLj2t2A", "Радіо Свобода Україна", "UCW5d-rpLATKOvBKs6heGuJw",
                   "SpastvRuchannel", "UC5azmFteRV-nj48bddT2z9w"]
    # x = test.get_channel_id("ХВАТИТМОЛЧАТЬРОССИЯ")
    # print(x)
    # test.video_stat(object_id="UC84J-P1AEat5jPz7C1vKhsw")
    test.monitor(channels=test_sample, interval=300, duration=48, delta=900)
    test.run()
    #  test.get_activity("UC84J-P1AEat5jPz7C1vKhsw", True)
