import os
import time
import argparse

def _parse_args():
  parser=argparse.ArgumentParser()
  parser.add_argument('path_to_log')
  parser.add_argument('interval')
  args=parser.parse_args()
  return args

args = _parse_args()

while True:
  os.system('clear')
  os.system('cat %s'%args.path_to_log)
  time.sleep(int(args.interval))
