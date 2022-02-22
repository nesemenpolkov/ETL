# -*- coding: utf-8 -*-
from collections import defaultdict
from common.templates import SEARCH, VIDEO_STATS, channel, video, CHANNEL, ACTIVITY, activity
from common.utils import from_url, jsonyfier, check_response, elapse_time, convert_time, time_delta
from extract.structures.YTFrame import YTFrame
import time, os


class VideoAPI:
    def __init__(self, API_KEY):
        self.api_key = API_KEY
        self.videos = defaultdict(list)
        self.params = channel(API_KEY)

    #  extracts all videos and its data from a channel TODO: интеграция в multiprocessing!
    def get_channel_videos(self, channelId, maxResults=10):
        if channelId is None:
            return False
        else:
            self.params.update({"channelId": channelId, "maxResults": maxResults})
        response = check_response(jsonyfier(from_url(SEARCH, params=self.params)))
        if response:
            nextPageToken = response.get("nextPageToken")
        else:
            return False

        print(f"Extracting videos from {channelId} ...")
        if nextPageToken:
            while nextPageToken:
                response = jsonyfier(from_url(SEARCH, params=self.params))
                self.__get_videos_list(response=response)
                nextPageToken = response.get("nextPageToken")
                self.params.update({"pageToken": nextPageToken})
        print(f"Extracted! {len(self.videos['id'])} notes.")
        return YTFrame(self.videos, channelId)

    #  support method for get_channel_videos
    def __get_videos_list(self, response=None):
        if response:
            for item in response.get("items", []):
                if item["id"]["kind"] == "youtube#video":
                    self.__to_dict(item=item)

    def __to_dict(self, item=None):
        if item:
            self.videos["publishedAt"].append(item["snippet"]["publishedAt"])
            self.videos["extractedAt"].append(elapse_time())
            self.videos["id"].append(item["id"]["videoId"])
            self.videos["title"].append(item["snippet"]["title"])
            #  self.videos["description"].append(item["snippet"]["description"]) --там что-то странное!
            self.__load_stats(item["id"]["videoId"])

    def __load_stats(self, videoId):
        stats = from_url(VIDEO_STATS, params=video(videoId=videoId,
                                                   API_KEY=self.api_key))
        stats = jsonyfier(stats)
        print(stats)
        self.videos["views"].append(stats["items"][0]["statistics"]["viewCount"])
        self.videos["likes"].append(stats["items"][0]["statistics"]["likeCount"])
        try:
            self.videos["comments"].append(stats["items"][0]["statistics"]["commentCount"])
        except:
            self.videos["comments"].append(None)

    # extract info from single video TODO: интеграция в multiprocessing!
    def from_video(self, videoId):
        print(f"Extracting data from video with id: {videoId} ...")
        outputs = {}
        self.params = video(videoId=videoId, API_KEY=self.api_key)
        self.params.update({"part": "snippet,statistics"})
        response = jsonyfier(from_url(VIDEO_STATS, params=self.params))
        response = response["items"][0]
        print(response)
        outputs["publishedAt"] = response["snippet"]["publishedAt"]
        outputs["extractedAt"] = elapse_time()
        outputs["title"] = response["snippet"]["title"]
        outputs["id"] = response["id"]
        outputs["description"] = response["snippet"]["description"]
        outputs["likes"] = response["statistics"]["likeCount"]
        outputs["views"] = response["statistics"]["viewCount"]
        outputs["comments"] = response["statistics"]["commentCount"]
        print("Extracted!")
        return YTFrame(outputs, videoId)
    
    def get_id(self, username):
        self.reset()
        if username:
            channelId = self.__get_channelName(username)
            if channelId:
                return channelId
        else:
            return None
    
    def __get_channelName(self, username):
        params = {"part": "id",
                  "key": self.api_key,
                  "forUsername": username}
        response = check_response(jsonyfier(from_url(CHANNEL, params=params)))
        #  print(response)
        if response:
            try:
                response.get("items")
                if response.get("items") is None:
                    return False
            except:
                return False
            for item in response.get("items"):
                if item["kind"] == "youtube#channel":
                    return item["id"]
        else:
            return False

    def scan_channel(self, channelId, period=48, interval=3600, scale=600):       #  TODO:add thread_name variable!
        print("[INSIDE]Thread started, with PID:", os.getpid(), "at:", str(elapse_time()))
        if channelId:
            start_time = elapse_time()
            result = None
            #print((elapse_time() - start_time) >= time_delta(hours=period))
            while (elapse_time() - start_time) <= time_delta(hours=period):    #  while start_time + timedelta(hours=period) > elapse_time():
                try:
                    result = self.activities(channelId, isMonitor=True)
                    if result is not None:
                        print(f"[NOTICE-FROM-{os.getpid()}]New video found on {channelId} channel, with id: {result}.")
                        break
                except OSError:
                    pass
                except ConnectionError:
                    pass
                except:
                    pass
                time.sleep(scale)
            self.collect_data(videoId=result, timeout=interval, period=period)
        print("[STOP]Thread:", os.getpid(), "at:", str(elapse_time()))

    def activities(self, channelId=None, isMonitor=False):
        if channelId:
            params = activity(channelId, self.api_key)
            if isMonitor:
                params.update({"publishedAfter": convert_time()})
            try:
                response = check_response(jsonyfier(from_url(ACTIVITY, params=params)))
            except:
                time.sleep(120)
                response = check_response(jsonyfier(from_url(ACTIVITY, params=params)))
        if response:
            print("[RESPONSE-TYPE]", type(response.get("items")))
            print("[RESPONSE-CASE]", response.get("items") == [])
            #nextPageToken = response.get("nextPageToken")
            if response["items"] != []:
                for item in response["items"]:
                    if item["snippet"]["type"] == "upload":
                        videoId = item["contentDetails"]["upload"]["videoId"]
                        print("[API-RESPONSE]", item)
                        return videoId
            elif response["items"] == []:
                return None
        else:
            return None
        #  а нужно ли?
        """if nextPageToken:
            while nextPageToken:
                break
                params.update({"pageToken": nextPageToken})
                response = jsonyfier(from_url(ACTIVITY, params=params))
                nextPageToken = response.get("nextPageToken")"""


    def collect_data(self, videoId=None, timeout=3600, period=48):
        if videoId:
            start = elapse_time()

            while time_delta(hours=period) >= (elapse_time() - start):  #  while start_time + timedelta(hours=period) > elapse_time():
                try:
                    self.__collectorman(videoId)
                except:
                    time.sleep(120)
                    self.collectorman(videoId)
                time.sleep(timeout)
        else:
            print("Bad videoId!")

    def __collectorman(self, videoId):
        params = video(videoId=videoId, API_KEY=self.api_key)
        store = {}
        try:
            response = check_response(jsonyfier(from_url(VIDEO_STATS, params=params)))
        except:
            time.sleep(120)
            response = check_response(jsonyfier(from_url(VIDEO_STATS, params=params)))
        response = response["items"][0]
        print("[SOURCE-API]", response)
        store["extractedAt"] = elapse_time()
        store["likes"] = response["statistics"]["likeCount"]
        store["views"] = response["statistics"]["viewCount"]
        try:
            store["comments"] = response["statistics"]["commentCount"]
        except:
            store["comments"] = None
        return YTFrame().add_to(row=store, filename="video@" + videoId)

    def search_name(self, contentId):
        if contentId:
            pass


    def reset(self):
        self.videos = defaultdict(list)
        self.params = channel(self.api_key)

if __name__ == "__main__":
    yt = VideoAPI("AIzaSyD49bsFeWc_Nvx-r5wuPy7RkPuiCFQN46E")
    #yt.activities("UC84J-P1AEat5jPz7C1vKhsw")
    yt.from_video(videoId="wAd5GHi9e2I").to_csv()
    #yt.get_channel_videos("UC84J-P1AEat5jPz7C1vKhsw").to_csv()
    #channelId = yt.get_id("АлексейНавальный")
    #print(channelId)
