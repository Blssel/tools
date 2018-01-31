#coding:utf-8

__author__='zhiyu yin '

from parse_fun import *

json_parser=dict()
json_parser['activity_net']=parse_activitynet
json_parser['kinetics']=parse_kinetics
json_parser['ava']=parse_ava

def parse_json_file(dataset,json_file):
    jf=json_parser[dataset]  # jf是用来解析dataset数据集的函数名
    return jf(json_file)
