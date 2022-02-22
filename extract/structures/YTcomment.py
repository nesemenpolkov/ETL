from config import supported_types, base_dir, storage_csv, storage_json
import pandas as pd
import os, csv, datetime
from common.utils import parse_request


#  уже не актуален!!!
class YTcomment:
    def __init__(self, payload, request=None):
        if type(payload) not in supported_types:
            raise TypeError(f"{type(payload)} is not supported as YTresult!")
        else:
            self.comment, self.reply = payload
        if request:
            content_type, content_id = parse_request(request=request)
            self.filename = "/" + "_".join(str(datetime.utcnow()).split()) + "_" + content_type + "_" + content_id

        self.save_csv = os.path.join(base_dir, storage_csv)
        self.save_json = os.path.join(base_dir, storage_json)
        os.makedirs(self.save_csv, exist_ok=True)
        os.makedirs(self.save_json, exist_ok=True)

    def to_csv(self):
        df1 = pd.DataFrame().from_dict(self.comment)
        df2 = pd.DataFrame().from_dict(self.reply)
        df1.to_csv(os.path.join(self.save_csv, self.filename + ".csv"))
        df2.to_csv(os.path.join(self.save_csv, self.filename + ".csv"))

    def to_json(self):
        self.comment = pd.json_normalize(self.comment, max_level=1)
        self.reply = pd.json_normalize(self.reply, max_level=1)
        df1 = pd.DataFrame().from_dict(self.comment)
        df2 = pd.DataFrame().from_dict(self.reply)
        df1.to_json(os.path.join(self.save_json, self.filename + ".json"))
        df2.to_json(os.path.join(self.save_json, self.filename + ".json"))

    def __str__(self):
        col_names = self.comment.keys()
        string_c = " ".join(col_names) + "\n"
        for i in range(len(self.comment[col_names[0]])):
            for title in self.comment.keys():
                string_c += str(self.comment[title][i])
            string_c += "\n"

        if self.reply:
            col_names = self.reply.keys()
            string_r = " ".join(col_names) + "\n"
            for i in range(len(self.reply[col_names[0]])):
                for title in self.reply.keys():
                    string_r += str(self.reply[title][i])
                string_r += "\n"
        return string_c + "\n" + string_r


if __name__ == "__main__":
    yt = YTcomment
