#coding:UTF-8

__author__='zhiyu yin'

import json
import os
import numpy as np
import cv2
import glob

'''
cal_det_frames_one_person_unify_bbox.py: 利用.json文件中存放的每一帧的人物坐标，将置信度最高的人物（默认为主角，后续再通过运动检测算法改进）单独抠出来，其它部分全部标零，然后保存图片到本地ucf-det-all-person文件夹中。
'''

JSON_PATH='/home/yzy/dataset/index-files/ucf-det-all-person-bbox-coordinate/ucf_bboxes_of_person_dict_*'
FRAME_PATH='/share/dataset/UCF101-frames-TSN'
SAVE_PATH='/home/yzy/dataset/ucf-det-all-person'

json_list=glob.glob(JSON_PATH)
json_list=sorted(json_list)
# 对于5个json中的每一个，分别读取并使用
for json_file in json_list:
    with open(json_file,'r') as f:
        print('loading {}'.format(json_file.split('/')[-1]))
        vid_dict=json.load(f)
        print('successfully loaded !')

    #遍历json，读取图片，标定并保存
    count=1
    for vid in vid_dict.keys():
        print count
        count+=1
        for img in vid_dict[vid].keys():
            #计算该帧路径，并读取
            img_path=os.path.join(FRAME_PATH,vid,img)
            src_img=cv2.imread(img_path)
            #创建全黑空白图片
            tar_img=np.zeros(src_img.shape,np.uint8)
            # 读取该帧中每一个检测到的人物坐标，将对应区域抠出来，贴放在全零背景上 
            # 先简单一点。。就以置信度最高的为准
            for i in range(len(vid_dict[vid][img])):
                #读取ROI
                bbox=vid_dict[vid][img][i]
                #放入ROI
                tar_img[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2]),:] =src_img[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2]),:]
                if i>=0:
                    break
            #保存图片
            if not os.path.exists(os.path.join(SAVE_PATH,vid)):
                os.mkdir(os.path.join(SAVE_PATH,vid))
            cv2.imwrite(os.path.join(SAVE_PATH,vid,img),tar_img)

