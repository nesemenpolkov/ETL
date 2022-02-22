from common.utils import yt_time, else_time


class Timeparser:
    def __init__(self, source_type):
        if source_type:
            if source_type == "youtube":
                self.format = yt_time
            elif source_type != "youtube":
                self.format = else_time
        else:
            self.format = yt_time

    def to_datetime(self, string=None):
        if string:
            time = self.format(time=string)
            return time
        else:
            return None
