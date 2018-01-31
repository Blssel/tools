#coding:UTF-8
import json
import os
import numpy as np
import cv2

JSON_PATH='/home/yzy/dataset/index-files/ucf-det-one-person-bbox-coordinate/ucf_bbox_of_person_dict.json'
FRAME_PATH='/share/dataset/UCF101-frames-TSN'
SAVE_PATH='/home/yzy/dataset/cnm'
#读取json
with open(JSON_PATH,'r') as f:
    vid_dict=json.load(f)

#遍历json，读取图片，标定并保存
count=1
for vid in vid_dict.keys():
    print count
    count+=1
    for img in vid_dict[vid].keys():
        #计算图片路径，并读取
        img_path=os.path.join(FRAME_PATH,vid,img)
        src_img=cv2.imread(img_path)
        #读取ROI
        bbox=vid_dict[vid][img]
        #创建全黑空白图片
        tar_img=np.zeros(src_img.shape,np.uint8)
        #放入ROI
        tar_img[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2]),:] =src_img[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2]),:]
        #保存图片
        if not os.path.exists(os.path.join(SAVE_PATH,vid)):
            os.mkdir(os.path.join(SAVE_PATH,vid))
        cv2.imwrite(os.path.join(SAVE_PATH,vid,img),tar_img)
