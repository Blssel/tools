#coding:utf-8
import cv2
import os
import os.path as osp
import glob
import argparse


def imgs2video(imgs_dir, save_path):
  imgs = glob.glob(os.path.join(imgs_dir, '*'))
  imgs.sort()

  tmp = cv2.imread(imgs[0])
  height = tmp.shape[0]
  width = tmp.shape[1]

  fps = 25
  fourcc = cv2.VideoWriter_fourcc(*'MJPG')
  video_writer = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

  for i, img in enumerate(imgs):
    path_to_img = img
    frame = cv2.imread(path_to_img)
    video_writer.write(frame)

  video_writer.release()

def parse_args():
  """parse arguments"""
  parser=argparse.ArgumentParser()
  parser.add_argument('src',help='Root path containing folders named like frames001.')
  parser.add_argument('dst',help='Saving ulr whose video is unavailable')
  parser.add_argument('img_format', help='the format of images for converting.')
  args=parser.parse_args()
  
  return args

def main():
  """
  frames001 is a folder hoding frames. This script convert frames to corresponding video frames001.avi
  """
  args = parse_args()
  src = args.src
  dst = args.dst
  img_format = args.img_format

  nums = 1
  for cur_location, folders, files in os.walk(src):
    if len(files) < 1:
      continue
    if files[0].split('.')[-1] != img_format:
      continue
    
    imgs_dir = cur_location
    video_name = cur_location.split(os.sep)[-1] + '.avi'
    save_path = osp.join(dst, video_name)
    
    print('Processing %dth video...'%nums)
    imgs2video(imgs_dir, save_path)    
    nums += 1
  print('Finished !!!')
 

if __name__ == '__main__':
  main()
