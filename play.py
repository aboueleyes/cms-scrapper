#!/usr/bin/env python

import argparse
import json
import os
from iterfzf import iterfzf

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=argparse.FileType('r'))
args = parser.parse_args()

f = args.i
s = f.read()
data = json.loads(s)
video_names = list(data.values())
to_be_downloaded = iterfzf(video_names)
index = video_names.index(to_be_downloaded)
link = list(data.keys())[index]
os.system(f'mpv {link}')