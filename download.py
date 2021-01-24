#!/usr/bin/env python

''' download
use youtube-dl to download videos
'''
import argparse
import json
import os

from iterfzf import iterfzf

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=argparse.FileType('r'))
args = parser.parse_args()

f = args.i
s = f.read()
s = s.replace('\'', '\"')
data = json.loads(s)
video_names = list(data.values())
to_be_downoaded = iterfzf(video_names, multi=True)

for item in to_be_downoaded:
    index = video_names.index(item)
    link = list(data.keys())[index]
    os.system(f'youtube-dl  "{link}" -o "{item}.mp4"')
