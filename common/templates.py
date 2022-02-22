#  Main YT DATA API requests URLs
ACTIVITY = f"https://www.googleapis.com/youtube/v3/activities"
SEARCH = f"https://www.googleapis.com/youtube/v3/search"
CHANNEL = f"https://www.googleapis.com/youtube/v3/channels"
VIDEO_STATS = f"https://www.googleapis.com/youtube/v3/videos"
FOR_COMMENTS = f"https://www.googleapis.com/youtube/v3/commentThreads"  # TODO: create a way to execute search by channel name


#  Main request parameters
def channel(API_KEY):
    FROM_CHANNEL = {
        "key": API_KEY,
        "part": "id,snippet",
    }
    return FROM_CHANNEL


def video(videoId, API_KEY):
    FROM_VIDEO = {
        "part": "statistics",
        "id": videoId,
        "key": API_KEY
    }
    return FROM_VIDEO


def comment(videoId, API_KEY, maxResult=100):
    FROM_COMMENT = {
        "part": "snippet,replies",
        "videoId": videoId,
        "key": API_KEY,
        "textFormat": "plainText",
        "maxResults": maxResult
    }
    return FROM_COMMENT


def activity(channelId, API_KEY, maxResult=100):
    FROM_ACTIV = {
        "part": "id,contentDetails,snippet",
        "key": API_KEY,
        "maxResults": maxResult,
        "channelId": channelId
    }
    return FROM_ACTIV


#  Templates for auto-filling dictionary TODO: add special function!
comment_terms = {
    "id": ["id"],
    "comment": ["snippet", "textDisplay"],
    "author": ["snippet", "authorDisplayName"],
    "likes": ["snippet", "likeCount"],
    "publishedAt": ["snippet", "publishedAt"]
}

replies_terms = {
    "parrentId": ["snippet", "parrentId"],
    "author": ["snippet", "authorDisplayName"],
    "replyComment": ["snippet", "textDisplay"],
    "publishedAt": ["snippet", "publishedAt"],
    "likes": ["snippet", "likeCount"]
}
