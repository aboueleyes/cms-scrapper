#!/usr/bin/env python

'''download use youtube-dl to download videos'''
import argparse
import json
import os
from iterfzf import iterfzf

parser = argparse.ArgumentParser()
parser.add_argument('-i','--input',type=argparse.FileType('r'),required=True)
args = parser.parse_args()

s = args.input.read()
data = json.loads(s)
video_names = list(data.values())
to_be_downoaded = iterfzf(video_names, multi=True)

for item in to_be_downoaded:
    index = video_names.index(item)
    link = list(data.keys())[index]
    command = f'ffmpeg-bar -i "{link}"  -bsf:a aac_adtstoasc\
    -vcodec copy -c copy -crf 50 "{item}.mp4"'
    os.system(command)
