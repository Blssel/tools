# tools
Some scripts written or used in my daliy life

# 函数列表及功能
- cal_det_frames_one_person_unify_bbox.py: 利用.json文件中存放的每一帧的人物坐标，将置信度最高的人物（默认为主角，后续再通过运动检测算法改进）单独抠出来，检测中心去取所有中心的平均，检测框尺寸同样取所有检测框的平均值，其它部分全部标零，然后保存图片到本地ucf-det-one-person-unify-bbox文件夹中(效果不太好)。

- cal_det_frames_max.py 每帧检测一个人，最后的结果是所有帧取并集，补全空白区域，剩下标零
- cal_det_frames_max_finetune.py  在上一个基础上进一步对过大的检测框进行缩小
- cal_det_frames.py 简单的每帧检测一个人，检测框就是原始的检测框
- cal_det_frames_cluster.py 使用ucf_bbox_of_person_dict.json文件，目的是使得在同一个视频中既能保留检测到的人，又尽可能精细地将它们突出出来。
> 具体做法：采用模仿聚类的方法，但是是聚类的简化版。算法流程是
``` python
for each bbox:
    if clusters_set==null:
        将该bbox作为第一个类别
    elif bbox dont blong to any cluster: # 以IOU作为判断标准，阈值设为80%
        将该bbox作为一个新的类别，并追加到类集合clusters_set中（类集合只需存放bbox即可，无需存对应img）
   
    else:
        for item in clusters_set:
            if bbox blong to item:
                追加到该item类别中
```
