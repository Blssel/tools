#coding:UTF-8
import json
import os
import numpy as np
import cv2
'''
 每张图片crop的位置恒定，为该段视频所有对人的bbox的上下左右最外围的位置
'''
JSON_PATH='/home/yzy/workspace/Faster-RCNN_TF/ucf_bbox_of_person_dict.json'
FRAME_PATH='/share/dataset/UCF101-frames-TSN'
SAVE_PATH='/home/yzy/dataset/ucf-det'
#读取json
with open(JSON_PATH,'r') as f:
    vid_dict=json.load(f)

#遍历json，读取图片，标定并保存
count=1
for vid in vid_dict.keys():
    print count
    count+=1
    #获得该视频统一的bbox
    final_bbox=[float('inf'),float('inf'),float('-inf'),float('-inf')]
    for img in vid_dict[vid].keys():
        bbox=vid_dict[vid][img]
        final_bbox[0]=min(vid_dict[vid][img][0],final_bbox[0])
        final_bbox[1]=min(vid_dict[vid][img][1],final_bbox[1])
        final_bbox[2]=max(vid_dict[vid][img][2],final_bbox[2])
        final_bbox[3]=max(vid_dict[vid][img][3],final_bbox[3])
    for img in vid_dict[vid].keys():
        #计算图片路径，并读取
        img_path=os.path.join(FRAME_PATH,vid,img)
        src_img=cv2.imread(img_path)
        #创建全黑空白图片
        tar_img=np.zeros(src_img.shape,np.uint8)
        #放入ROI
        tar_img[int(final_bbox[1]):int(final_bbox[3]),int(final_bbox[0]):int(final_bbox[2]),:] =src_img[int(final_bbox[1]):int(final_bbox[3]),int(final_bbox[0]):int(final_bbox[2]),:]
        #保存图片
        if not os.path.exists(os.path.join(SAVE_PATH,vid)):
            os.mkdir(os.path.join(SAVE_PATH,vid))
        cv2.imwrite(os.path.join(SAVE_PATH,vid,img),tar_img)

