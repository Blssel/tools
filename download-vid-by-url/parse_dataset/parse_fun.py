# coding:utf-8

__author__='zhiyu yin'

import json

def parse_activitynet(json_file):

    with open(json_file,'r') as f:
        json_data=json.load(f)

    vid_list=[]
    for i in json_data['database'].keys():
        id_url=i+ '  '+ json_data['database'][i]['url']
        vid_list.append(id_url)

    return vid_list



def parse_kinetics(json_file):
    with open(json_file,'r') as f:
        json_data=json.load(f)

    vid_list=[]
    for vid_id in json_data.keys():
        id_url=vid_id+ '  '+ json_data[vid_id]['url']
        vid_list.append(id_url)

    return vid_list


def parse_ava(json_file):
    return
