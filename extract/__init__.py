from extract.youtube.youtube_comments import CommentAPI
from extract.youtube.youtube_videos import VideoAPI
from extract.structures.YTFrame import YTFrame
import threading
from common.utils import elapse_time, time_delta


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
        for key in kwargs.key():
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

    def monitor(self, channels=[], interval=600, duration=48, delta=3600, isInfinite=False):
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
        threads = []
        start_time = elapse_time()
        channels = self.channels
        execs = VideoAPI(self.settings["key"])
        print("Scan procedure started at", str(elapse_time()))
        while channels != []:
            for ch in channels:
                new_thread = threading.Thread(target=execs.scan_channel, args=(
                    ch, self.settings["duration"], self.settings["timeDelta"], self.settings["timeInterval"]))
                new_thread.setDaemon(True)
                new_thread.start()
                #  print(new_thread.getName(), "status:", new_thread.is_alive())
                threads.append((new_thread, ch))
                channels.remove(ch)
        stime = elapse_time()
        while threads != []:

            for thread, _ in threads:
                if not thread.is_alive():
                    if time_delta(hours=self.settings["duration"]) < elapse_time() - start_time:
                        print(thread.getName(), "is down!")
                        threads.remove(thread)
                    else:
                        thread.start()

            if elapse_time() - stime > time_delta(seconds=self.settings["timeInterval"]):
                print(elapse_time())
                stime = elapse_time()
                print("Next check at:", stime + time_delta(seconds=self.settings["timeInterval"]))
        print(f"Monitoring is finished. Proceed time: {elapse_time() - start_time}.")

    def run(self, isBackground=False):

        if isBackground:
            m_thread = threading.Thread(target=self.__thread_maker)
            m_thread.setDaemon(True)
            m_thread.start()
        else:
            self.__thread_maker()
        #  ___________________________________
        #  place for additional code
        #  ___________________________________
        #  last thing in this method
        if isBackground:
            m_thread.join()

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
    test.monitor(channels=test_sample, interval=300, duration=48)
    test.run()
    #  test.get_activity("UC84J-P1AEat5jPz7C1vKhsw", True)
