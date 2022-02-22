# -*- coding: utf-8 -*-
from collections import defaultdict
from common.templates import channel, FOR_COMMENTS, comment
from common.utils import from_url, jsonyfier, check_response, elapse_time
from extract.structures.YTFrame import YTFrame


class CommentAPI:
    def __init__(self, API_KEY):
        self.api_key = API_KEY
        self.replies = defaultdict(list)
        self.params = comment(API_KEY=self.api_key, videoId=None)
        self.comments = defaultdict(list)

    def get_video_comments(self, videoId):
        if videoId is None:
            return False
        else:
            self.params.update({"videoId": videoId})
        response = check_response(jsonyfier(from_url(FOR_COMMENTS, params=self.params)))
        if response:
            self.__load_stats(response["items"])
            nextPageToken = response.get("nextPageToken")
        else:
            return False
        if nextPageToken:
            while nextPageToken:
                self.params.update({"pageToken": nextPageToken})
                response = jsonyfier(from_url(FOR_COMMENTS, params=self.params))
                nextPageToken = response.get("nextPageToken")
                self.__load_stats(response["items"])
        return YTFrame(self.comments, self.replies, videoId)


    def __to_dict(self, comment=None, reply=None):
        if comment:
            self.comments["id"].append(comment["id"])
            self.comments["extractedAt"].append(elapse_time())
            self.comments["comment"].append(comment["snippet"]["textDisplay"])
            self.comments["author"].append(comment["snippet"]["authorDisplayName"])
            self.comments["likes"].append(comment["snippet"]["likeCount"])
            self.comments["publishedAt"].append(comment["snippet"]["publishedAt"])
        elif reply:
            self.replies["parentId"].append(reply["snippet"]["parentId"])
            self.replies["authorDisplayName"].append(reply["snippet"]["authorDisplayName"])
            self.replies["replyComment"].append(reply["snippet"]["textDisplay"])
            self.replies["publishedAt"].append(reply["snippet"]["publishedAt"])
            self.replies["extractedAt"].append(elapse_time())
            self.replies["likeCount"].append(reply["snippet"]["likeCount"])

    def __load_stats(self, items):
        for item in items:
            self.__to_dict(comment=item["snippet"]["topLevelComment"])

            if "replies" in item.keys():
                for reply in item["replies"]["comments"]:
                    self.__to_dict(reply=reply)

    def reset(self):
        self.comments = defaultdict(list)
        self.replies = defaultdict(list)
        self.params = channel(self.api_key)

if __name__ == "__main__":
    yt = CommentAPI("AIzaSyD49bsFeWc_Nvx-r5wuPy7RkPuiCFQN46E")
    yt.get_video_comments("w8O6apM3aBw").to_csv()
    #yt.get_video_comments("UCrrwDQIk4Qys3O9CvoGAYuQ").to_csv()

