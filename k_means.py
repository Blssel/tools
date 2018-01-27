#coding:utf-8

__author__='zhiyu yin'

import numpy as np

def cal_avg_bbox(bbox_list):
    sum_bbox=np.array([0.0, 0.0, 0.0, 0.0])
    bbox_list=np.array(bbox_list)
    for i in range(len(bbox_list)):
        sum_bbox+=bbox_list[i]
    avg_bbox=sum_bbox/len(bbox_list)
    avg_bbox=avg_bbox.tolist()
    return avg_bbox

def add_new_cluster(cluster_set,bbox,cluster_num):
    cluster_set['cluster_'+str(cluster_num)]={}
    cluster_set['cluster_'+str(cluster_num)]['bboxes']=[]
    cluster_set['cluster_'+str(cluster_num)]['bboxes'].append(bbox)
    cluster_set['cluster_'+str(cluster_num)]['avg_bbox']=cal_avg_bbox(cluster_set['cluster_'+str(cluster_num)]['bboxes']) # 等于所有bbox各项平均值    
    return cluster_set
'''
def cal_overlap_area(avg_bbox,bbox):
def cal_iou(avg_bbox,bbox):
    area_avg_bbox=(avg_bbox[3]-avg_bbox[1])*(avg_bbox[2]-avg_bbox[0])
    area_bbox=(bbox[3]-bbox[1])*(bbox[2]-bbox[0])
    overlap_area=cal_overlap_area(avg_bbox,bbox)
    sum_area=area_avg_bbox+area_bbox-overlap_area
    iou=overlap_area/sum_area
    return iou
'''
def calcIOU(avg_bbox,bbox):
    one_x=avg_bbox[0]
    one_y=avg_bbox[1] 
    one_w=avg_bbox[2]-avg_bbox[0] 
    one_h=avg_bbox[3]-avg_bbox[1]

    two_x=bbox[0]
    two_y=bbox[1] 
    two_w=bbox[2]-bbox[0] 
    two_h=bbox[3]-bbox[1]

    if((abs(one_x - two_x) < ((one_w + two_w) / 2.0)) and (abs(one_y - two_y) < ((one_h + two_h) / 2.0))):  
        lu_x_inter = max((one_x - (one_w / 2.0)), (two_x - (two_w / 2.0)))  
        lu_y_inter = min((one_y + (one_h / 2.0)), (two_y + (two_h / 2.0)))  
  
        rd_x_inter = min((one_x + (one_w / 2.0)), (two_x + (two_w / 2.0)))  
        rd_y_inter = max((one_y - (one_h / 2.0)), (two_y - (two_h / 2.0)))  
  
        inter_w = abs(rd_x_inter - lu_x_inter)  
        inter_h = abs(lu_y_inter - rd_y_inter)  
  
        inter_square = inter_w * inter_h  
        union_square = (one_w * one_h) + (two_w * two_h) - inter_square  
  
        calcIOU = inter_square / union_square * 1.0  
        #print("calcIOU:", calcIOU)
        return calcIOU
    else:  
        #print("No intersection!")
        return None
  
    return calcIOU

def isMatch(avg_bbox,bbox):
    iou=calcIOU(avg_bbox,bbox)
    if iou==None:
        return (False,None)
    elif iou>=0.1:
        return (True,iou)
    else: 
        return (False,None)
def blongto(cluster_set,bbox):
    # 如果cluster_set为空
    if not cluster_set:
        return None
    # 否则与逐个类别的avg_bbox对比，满足IOU80%则返回类名，若无满足的，返回None
    else:
        max_iou=-0.1
        most_matched=None
        for i in cluster_set.keys():
            ismatch=isMatch(cluster_set[i]['avg_bbox'],bbox)
            if ismatch[0]:  #如果匹配，则选出最匹配的那个类返回
                if ismatch[1]>max_iou:
                    max_iou=ismatch[1]
                    most_matched=i
        if most_matched!= None:
            return most_matched
        else:
            return None

def insert_into_existing_cluster(cluster_set,bbox,cluster_name):
    cluster_set[cluster_name]['bboxes'].append(bbox)
    # 顺便还要更新avg_bbox
    cluster_set[cluster_name]['avg_bbox']=cal_avg_bbox(cluster_set[cluster_name]['bboxes']) 
    return cluster_set

# for each vid 先判断将这些bbox进行聚类，（IOU阈值设为80%）
def cluster_bbox(vid_dict,vid):
    cluster_num=1  #标号从1开始
    cluster_set={}
    for img in vid_dict[vid].keys():
        bbox=vid_dict[vid][img]
        # 判断bbox属于哪一个类，返回对应类名，若都不属于，返回None
        cluster_name=blongto(cluster_set,bbox)
        # 若都不属于，则新增类，否则插入相应类中
        if cluster_name==None:
            cluster_num+=1
            cluster_set=add_new_cluster(cluster_set,bbox,cluster_num)
        else:
            cluster_set=insert_into_existing_cluster(cluster_set,bbox,cluster_name)

    return cluster_set
