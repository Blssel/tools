#coding:UTF-8
import json
import os

JSON_PATH='/home/yzy/workspace/Faster-RCNN_TF/ucf_bbox_of_person_dict.json'
SAVE_PATH='/home/yzy/dataset/ucf-det2'
#读取json
with open(JSON_PATH,'r') as f:
    vid_dict=json.load(f)

#遍历json，读取图片，标定并保存
for vid in vid_dict.keys():
    
