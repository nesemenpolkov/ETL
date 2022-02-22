from collections import defaultdict, namedtuple
import os

# ////////////////////////////////////IMPORTANT\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#
#
#   file_name template should be like:
#       source_id_date.extension
#
#     source -> youtube, yandex and etc...
#       id -> id of the video, that was used in parsing
#           data -> some string of a date for i.g: 2018-05-13-11-13-22
#               .extension -> .csv or .json, it is a temporary files
#                   and the final version of data will be represented in
#                       Data Base files!!!!
#
#
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\////////////////////////////////////////////




# YTFrame configs
supported_types = [type(defaultdict(list)), type(defaultdict), type(list), type(dict), type(namedtuple), type(tuple), type(set), type({}), type(())]
base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)))

storage_csv = "warhouse\\data-csv"
storage_json = "warhouse\\data-json"
accumulator = "warhouse\\accumulator"

#  Timeparse configs        TODO: Make type format of types automatic
default_format = "youtube"