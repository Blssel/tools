# coding:utf-8
import numpy as np
import cv2
import math
import json
import os

def _cal_deta(bbox):
    bbox_size=(bbox[2]-bbox[0])*(bbox[3]-bbox[1])
    #print bbox_size
    k=50.0/3600.0
    deta=k*bbox_size
    return deta	
# ¿¿¿map¿¿¿
def _normalize(weight_map):
    map_min, map_max=weight_map.min(), weight_map.max()
    weight_map=(weight_map-map_min)/(map_max-map_min)
    return weight_map

# ¿¿¿¿weight map¿¿¿¿¿bbox¿¿¿¿¿¿¿¿¿¿¿¿¿¿bbox¿¿¿¿¿¿¿gauss¿¿¿¿¿¿¿weight¿
# ¿¿¿¿¿gauss¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿
# ¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿1¿¿¿¿¿¿¿¿¿¿¿
def generate_2d_gauss_matrix(weight_map,bbox):
    # decide ¿ , ¿ should be the function of the size of bbox. The smaller the size of bbox is , the faster the value decay
    im_size=weight_map.shape
    deta=_cal_deta(bbox)
    # ¿¿¿¿¿¿¿¿¿
    center_coordinate=(bbox[1]+(bbox[3]-bbox[1])/2, 
	                   bbox[0]+(bbox[2]-bbox[0])/2)
    # ¿¿¿¿¿¿¿¿¿
    weight_map_tmp=np.array([[0.0]*im_size[1]]*im_size[0])
    for i in range(im_size[0]):
        for j in range(im_size[1]):
            a=pow(i-center_coordinate[0],2)
            b=pow(j-center_coordinate[1],2)
            c=a+b
            weight_map_tmp[i][j]=pow(math.e,-c/(2*pow(deta,2)))
    # ¿weight_map_tmp¿¿¿weight_map¿¿¿¿¿¿weight_map
    weight_map=_normalize(weight_map+weight_map_tmp)
    weight_map[(weight_map)<0.4]=0
#    weight_map=weight_map*1.2
    return weight_map

	
def main():
    JSON_PATH='/home/yzy/dataset/index-files/ucf-det-all-person-bbox-coordinate/ucf_bboxes_of_person_dict_5.json'
    FRAME_PATH='/share/dataset/UCF101-frames-TSN'
    SAVE_PATH='/home/yzy/dataset/tmp'
    #¿¿json
    with open(JSON_PATH,'r') as f:
        vid_dict=json.load(f)

    #¿¿json¿¿¿¿¿¿¿¿¿¿¿
    count=1
    for vid in vid_dict.keys():
        print count
        count+=1
        for img in vid_dict[vid].keys():
            # ¿¿¿¿¿¿¿¿¿¿
            img_path=os.path.join(FRAME_PATH,vid,img)
            src_img=cv2.imread(img_path)
            # ¿¿¿¿weight_map
            weight_map=np.array([[0.0]*src_img.shape[1]]*src_img.shape[0]) 
            for i in range(len(vid_dict[vid][img])):
                # ¿¿ROI
                bbox=vid_dict[vid][img][i]
                weight_map=generate_2d_gauss_matrix(weight_map, bbox)
                if i>=2:
                    break

            #print weight_map[100]
            weight_map_3_channels=np.dstack([weight_map, weight_map,weight_map])

            tar_img= np.uint8(src_img* weight_map_3_channels)
            # ¿¿¿¿
            if not os.path.exists(os.path.join(SAVE_PATH,vid)):
                os.mkdir(os.path.join(SAVE_PATH,vid))
            cv2.imwrite(os.path.join(SAVE_PATH,vid,img),tar_img)


if __name__== '__main__':
    main()
