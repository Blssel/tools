#coding:UTF-8
import json
import os
import numpy as np
import cv2

JSON_PATH='/home/yzy/dataset/index-files/ucf-det-one-person-bbox-coordinate/ucf_bbox_of_person_dict.json'
FRAME_PATH='/share/dataset/UCF101-frames-TSN'
SAVE_PATH='/home/yzy/dataset/ucf-det-one-person-unify-bbox'
#读取json
with open(JSON_PATH,'r') as f:
    vid_dict=json.load(f)

#遍历json，读取图片，标定并保存
count=1
for vid in vid_dict.keys():
    print count
    count+=1
    # 先算该视频下所有帧的平均高和宽 和 所有帧检测中心的平均
    sum_height=0.0
    sum_width=0.0
    sum_height_coordinate=0.0
    sum_width_coordinate=0.0
    for img in vid_dict[vid].keys():
        sum_height=sum_height+(vid_dict[vid][img][3]-vid_dict[vid][img][1])
        sum_width=sum_height+(vid_dict[vid][img][2]-vid_dict[vid][img][0])
        sum_height_coordinate+=vid_dict[vid][img][1]+(vid_dict[vid][img][2]-vid_dict[vid][img][0])/2
        sum_width_coordinate+=vid_dict[vid][img][0] +(vid_dict[vid][img][3]-vid_dict[vid][img][1])/2
    avg_height=sum_height/len(vid_dict[vid].keys())
    avg_width=sum_width/len(vid_dict[vid].keys())
    avg_height_coordinate=sum_height_coordinate/len(vid_dict[vid].keys())
    avg_width_coordinate=sum_width_coordinate/len(vid_dict[vid].keys())
    center_coordinate=(avg_height_coordinate, avg_width_coordinate) # 计算中央坐标(横坐标对应高度上的中心位置，纵坐标对应宽度上的中心位置)

    for img in vid_dict[vid].keys():
        # 计算图片路径，并读取
        img_path=os.path.join(FRAME_PATH,vid,img)
        src_img=cv2.imread(img_path)
        # 计算新的bbox  取名final_bbox
        final_bbox=[]
        final_bbox.append(center_coordinate[1]-avg_width/2)
        final_bbox.append(center_coordinate[0]-avg_height/2)
        final_bbox.append(center_coordinate[1]+avg_width/2)
        final_bbox.append(center_coordinate[0]+avg_height/2)
        # 创建全黑空白图片
        tar_img=np.zeros(src_img.shape,np.uint8)
        # 放入ROI
        tar_img[int(final_bbox[1]):int(final_bbox[3]),int(final_bbox[0]):int(final_bbox[2]),:] =src_img[int(final_bbox[1]):int(final_bbox[3]),int(final_bbox[0]):int(final_bbox[2]),:]
        # 保存图片
        if not os.path.exists(os.path.join(SAVE_PATH,vid)):
            os.mkdir(os.path.join(SAVE_PATH,vid))
        cv2.imwrite(os.path.join(SAVE_PATH,vid,img),tar_img)

