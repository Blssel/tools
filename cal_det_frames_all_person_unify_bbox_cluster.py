#coding:UTF-8

__author__='zhiyu yin'

import json
import os
import numpy as np
import cv2
import k_means
import gauss_masking

JSON_PATH='/home/yzy/dataset/index-files/ucf-det-one-person-bbox-coordinate/ucf_bbox_of_person_dict.json'
FRAME_PATH='/share/dataset/UCF101-frames-TSN'
SAVE_PATH='/home/yzy/dataset/tmp2'
#读取json
with open(JSON_PATH,'r') as f:
    vid_dict=json.load(f)

#遍历json，读取图片，标定并保存
count=1
for vid in vid_dict.keys():
    print 'addressing %dth vid'%count
    count+=1

    cluster_set=k_means.cluster_bbox(vid_dict,vid)
    print '%d clusters included in this vid'%len(cluster_set.keys())
    # 依据cluster_set 中的avg_bbox,生成蒙版
    #tmp_img_path=os.path.join(FRAME_PATH,vid,vid_dict[vid][vid_dict[vid].keys()[0]])
    tmp_img_path=os.path.join(FRAME_PATH,vid,'img_00001.jpg')
    tmp_img=cv2.imread(tmp_img_path)
    weight_map=np.array([[0.0]*tmp_img.shape[1]]*tmp_img.shape[0]) #先生成一个全零蒙版
    
    for i in cluster_set.keys():
        weight_map=gauss_masking.generate_2d_gauss_matrix(weight_map, cluster_set[i]['avg_bbox'])

    for img in vid_dict[vid].keys():
        # 计算图片路径，并读取
        img_path=os.path.join(FRAME_PATH,vid,img)
        src_img=cv2.imread(img_path)
        weight_map_3_channels=np.dstack([weight_map, weight_map,weight_map])
        tar_img=np.uint8(src_img*weight_map_3_channels)
        # 保存图片
        if not os.path.exists(os.path.join(SAVE_PATH,vid)):
            os.mkdir(os.path.join(SAVE_PATH,vid))
        cv2.imwrite(os.path.join(SAVE_PATH,vid,img),tar_img)

