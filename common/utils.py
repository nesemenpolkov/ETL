import json
import requests
from datetime import datetime, timedelta
from inspect import currentframe


def jsonyfier(response):
    return json.loads(response.text)


def from_url(url, params=None):
    return requests.get(url, params)


def check_response(response=None):
    if response:
        #  print(response)
        try:
            if "error" in response:
                raise Exception("Cannot execute the request!")
        except Exception as e:
            print(e)
            return False
        return response


def converttime(time=None):
    if time:
        date, time = time.split("T")[0], time.split("T")[1]

def get_request(type=None, id=None):
    if type not in ["video", "videos", "comments", "replies"]:
        return Exception("Bad request type found!")
    return "@".join([type, id])

def parse_request(request):
    return request.split("@")[0], request.split("@")[1]

#  unusefull function
def check_args(x):
    cl = currentframe().f_back.f_locals
    print(cl)
    print(*[name for name, value in cl.items() if x is value])
    return x

def yt_time(time=None):
    time = time.replace("T", " ").replace("Z", " ").replace(":", " ").replace("-", " ").split()
    return datetime.strptime(" ".join(time), "%Y %m %d %H %M %S")

def elapse_time():
    return datetime.utcnow()

def convert_time(time=datetime.utcnow(), backward=False):
    if not backward:
        return str(time).replace(" ", "T") + "Z"

def refurbish(value=None):
    if value:
        if value < 0:
            return abs(value)

def time_delta(hours=0, minutes=0, seconds=0):
    return timedelta(seconds=seconds, minutes=minutes, hours=hours)

if __name__ == "__main__":
    yt_time()