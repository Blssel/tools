#coding:UTF-8
import json
import os
import numpy as np
import cv2

JSON_PATH='/home/yzy/workspace/Faster-RCNN_TF/ucf_bbox_of_person_dict.json'
FRAME_PATH='/share/dataset/UCF101-frames-TSN'
SAVE_PATH='/home/yzy/dataset/ucf-det2'
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
        frame_num=img.split('_')[1]
        flow_x_path=os.path.join(FRAME_PATH,vid,'flow_x_'+frame_num)
        flow_y_path=os.path.join(FRAME_PATH,vid,'flow_y_'+frame_num)
        flow_warped_x_path=os.path.join(FRAME_PATH,vid,'flow_warped_x_'+frame_num)
        flow_warped_y_path=os.path.join(FRAME_PATH,vid,'flow_warped_y_'+frame_num)
        if not (os.path.exists(flow_x_path) and os.path.exists(flow_y_path) and os.path.exists(flow_warped_x_path) and os.path.exists(flow_warped_y_path)):
            continue
        src_img_flow_x=cv2.imread(flow_x_path)
        src_img_flow_y=cv2.imread(flow_y_path)
        src_img_flow_warped_x=cv2.imread(flow_warped_x_path)
        src_img_flow_warped_y=cv2.imread(flow_warped_y_path)
        #读取ROI
        bbox=vid_dict[vid][img]
        #创建全黑空白图片
        tar_img_flow_x=np.zeros(src_img_flow_x.shape,np.uint8)
        tar_img_flow_y=np.zeros(src_img_flow_y.shape,np.uint8)
        tar_img_flow_warped_x=np.zeros(src_img_flow_warped_x.shape,np.uint8)
        tar_img_flow_warped_y=np.zeros(src_img_flow_warped_y.shape,np.uint8)
        #放入ROI
        tar_img_flow_x[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2]),:] =src_img_flow_x[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2]),:]
        tar_img_flow_y[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2]),:] =src_img_flow_y[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2]),:]
        tar_img_flow_warped_x[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2]),:] =src_img_flow_warped_x[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2]),:]
        tar_img_flow_warped_y[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2]),:] =src_img_flow_warped_y[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2]),:]
        #保存图片
        if not os.path.exists(os.path.join(SAVE_PATH,vid)):
            os.mkdir(os.path.join(SAVE_PATH,vid))
        cv2.imwrite(os.path.join(SAVE_PATH,vid,'flow_x_'+frame_num),tar_img_flow_x)
        cv2.imwrite(os.path.join(SAVE_PATH,vid,'flow_y_'+frame_num),tar_img_flow_y)
        cv2.imwrite(os.path.join(SAVE_PATH,vid,'flow_warped_x_'+frame_num),tar_img_flow_warped_x)
        cv2.imwrite(os.path.join(SAVE_PATH,vid,'flow_warped_y_'+frame_num),tar_img_flow_warped_y)

