import pandas as pd
from transform import Timeparser


class Transformer:
    def __init__(self, filename=None):
        if filename:
            self.filename = filename

    def open_file(self, filename):
        if filename:
            self.filename = filename
            if self.filename.endwith(".csv"):
                self.df = pd.read_csv(self.filename, index_col=0)
            elif self.filename.endwith(".json"):
                self.df = pd.read_json(self.filename)

    def __fetch_time(self, source_type):
        time_stamp = Timeparser(source_type=source_type)
        col_names = self.df.keys()
        for name in col_names:
            if name in ["publishedAt", "date", "Date", "publish time"]:
                self.df["publishedAt"] = self.df["publishedAt"].apply(time_stamp.to_datetime)

    def __filler(self, isMonitor=False):
        if not isMonitor:
            self.df = self.df.sort_values(by="extractedAt", ignore_index=True, ascending=False)
            self.df = self.df.dropna(axis=1)
            self.df = self.df.drop_duplicates()

    def __admit(self):
        columns = [name for name in self.df.columns if df[name].dtypes == "int64"]
        for column in columns:
