from config import supported_types, base_dir, storage_csv, storage_json, accumulator
import pandas as pd
import os, csv
from datetime import datetime
from collections import defaultdict


class YTFrame:
    def __init__(self, *args):
        # for arg in range(len(args) - 1):
        # if arg not in supported_types:
        # raise Exception(f"Object with type {type(arg)} is unsupported in YTFrame!")
        if len(args) == 3:
            self.comments, self.replies, self.content_id = args
            self.type = "comment&reply"
            self.filename = f"youtube-{self.type}-{'_'.join(str(datetime.utcnow()).replace('.', ':').replace(':', '-').split())}-{self.content_id}"
        elif len(args) == 2:
            self.payload, self.content_id = args
            self.type = "video"
            self.filename = f"youtube-{self.type}-{'_'.join(str(datetime.utcnow()).replace('.', ':').replace(':', '-').split())}-{self.content_id}"
        elif len(args) == 0:
            print(os.path.abspath("../"))

        #  self.filename = f"/{'_'.join(str(datetime.datetime.utcnow()).replace('.', ':').split())}_{self.type}_{self.content_id}"
        self.save_csv = os.path.join(base_dir, storage_csv)
        self.save_json = os.path.join(base_dir, storage_json)
        self.append_csv = os.path.join(base_dir, accumulator)
        print(self.save_csv)
        os.makedirs(self.save_csv, exist_ok=True)
        os.makedirs(self.save_json, exist_ok=True)
        os.makedirs(self.append_csv, exist_ok=True)

    def to_csv(self, sourceImportance=True):
        if self.type == "video":
            if isinstance(self.payload, defaultdict):
                if not os.path.exists(self.save_csv):
                    return False
                df = pd.DataFrame().from_dict(self.payload)
            elif isinstance(self.payload, dict):
                df = pd.DataFrame().from_records([self.payload])
            df.to_csv(os.path.join(self.save_csv, self.filename + ".csv"))
        elif self.type == "comment&reply":
            df1 = pd.DataFrame().from_dict(self.comments)
            df2 = pd.DataFrame().from_dict(self.replies)
            df1.to_csv(os.path.join(self.save_csv, self.filename + ".csv"))
            df2.to_csv(os.path.join(self.save_csv, self.filename + ".csv"))
        print("Saved to:", os.path.join(self.save_csv, self.filename + ".csv"))

    def to_json(self, sourceImportance=True):
        if self.type == "video":
            # self.payload = pd.json_normalize(self.payload, max_level=1) <-- либо это либо через DF в явном виде!
            if not os.path.exists(self.save_json):
                return False
            df = pd.DataFrame().from_dict(self.payload)
            df.to_json(os.path.join(self.save_json, self.filename + ".json"))
        elif self.type == "comment/reply":
            self.comment = pd.json_normalize(self.comments, max_level=1)
            self.reply = pd.json_normalize(self.replies, max_level=1)
            df1 = pd.DataFrame().from_dict(self.comments)
            df2 = pd.DataFrame().from_dict(self.replies)
            df1.to_json(os.path.join(self.save_json, self.filename + ".json"))
            df2.to_json(os.path.join(self.save_json, self.filename + ".json"))
        print("Saved to:", os.path.join(self.save_json, self.filename + ".json"))

    def __str__(self):
        if self.type == "video":
            col_names = self.payload.keys()
            string = " ".join(col_names) + "\n"
            for i in range(len(self.payload[col_names[0]])):
                for title in self.payload.keys():
                    string += str(self.payload[title][i])
                string += "\n"
            return string
        elif self.type == "comment/reply":
            col_names = self.comment.keys()
            string_c = " ".join(col_names) + "\n"
            string_r = None
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

    def add_to(self, row=None, filename=None):
        if not filename.endswith(".csv"):
            filename = filename + ".csv"
        if not os.path.exists(os.path.join(self.append_csv, filename)):
            with open(os.path.join(self.append_csv, filename), "w") as header:
                head = csv.DictWriter(header, fieldnames=list(row.keys()), delimiter=",")
                head.writeheader()
                head.writerow(row)
        else:
            with open(os.path.join(self.append_csv, filename), "a") as file:
                data = csv.DictWriter(file, fieldnames=list(row.keys()), delimiter=",")
                data.writerow(row)


if __name__ == "__main__":
    data = {
        "date": "10 may 1999",
        "likes": 10,
        "views": 15,
        "comments": 12
    }
    yt = YTFrame().add_to(data, "test1")
