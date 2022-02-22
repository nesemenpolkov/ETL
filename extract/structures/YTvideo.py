from config import supported_types, base_dir, storage_csv, storage_json
import pandas as pd
import os, csv, datetime
from common.utils import parse_request, check_args


class YTvideo:
    def __init__(self, payload, request=None):
        check_args(payload)
        if type(payload) not in supported_types:
            raise TypeError(f"{type(payload)} is not supported as YTresult!")
        else:
            self.payload = payload
        if request:
            content_type, content_id = parse_request(request=request)
            self.filename = "/" + "_".join(str(datetime.datetime.utcnow()).split()) + "_" + content_type + "_" + content_id

        self.save_csv = os.path.join(base_dir, storage_csv)
        self.save_json = os.path.join(base_dir, storage_json)
        os.makedirs(self.save_csv, exist_ok=True)
        os.makedirs(self.save_json, exist_ok=True)

    def to_csv(self):
        print(self.save_csv)
        if not os.path.exists(self.save_csv):
            return False
        df = pd.DataFrame().from_dict(self.payload)
        df.to_csv(os.path.join(self.save_csv, self.filename + ".csv"))

    def to_json(self):
        self.payload = pd.json_normalize(self.payload, max_level=1)
        if not os.path.exists(self.save_json):
            return False
        df = pd.DataFrame().from_dict(self.payload)
        df.to_json(os.path.join(self.save_json, self.filename + ".json"))

    def __str__(self):
        col_names = self.payload.keys()
        string = " ".join(col_names) + "\n"
        for i in range(len(self.payload[col_names[0]])):
            for title in self.payload.keys():
                string += str(self.payload[title][i])
            string += "\n"
        return string