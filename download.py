import os 
import json
import argparse 

from iterfzf import iterfzf 

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=argparse.FileType('r'))
args = parser.parse_args()
f = args.i
s = f.read()
s = s.replace('\'','\"')
data = json.loads(s)
video_names = list(data.values())
