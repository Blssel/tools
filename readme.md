# tools
Some scripts written or used in my daliy life

# 函数列表及功能

## 转化原始帧为只保留被检测算法检测到的人物（做det-tsn实验用）

涉及到的几个文件分别对应不同的需求，依据对保留情况的不同而不同

- cal_det_frames_one_person_unify_bbox.py: 利用.json文件中存放的每一帧的人物坐标，将置信度最高的人物（默认为主角，后续再通过运动检测算法改进）单独抠出来，检测中心去取所有中心的平均，检测框尺寸同样取所有检测框的平均值，其它部分全部标零，然后保存图片到本地ucf-det-one-person-unify-bbox文件夹中(效果不太好)。

- **cal_det_frames_max.py** 每帧检测一个人，最后的结果是所有帧取并集，补全空白区域，剩下标零
- cal_det_frames_max_finetune.py  在上一个基础上进一步对过大的检测框进行缩小
- cal_det_frames.py 简单的每帧检测一个人，检测框就是原始的检测框
- **cal_det_frames_cluster.py** 使用ucf_bbox_of_person_dict.json文件，目的是使得在同一个视频中既能保留检测到的人，又尽可能精细地将它们突出出来。
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

## 下载youtube上的数据集（youtube-dl工具）

现在许多动作识别数据集，涉及到的数据量巨大，而且由于版权的缘故，往往仅提供视频的URL，这就要求我们自己下载，下面的工具可以依据URL下载视频，目前仅限youtube上的视频

所有文件都在download-vid-by-url文件夹中，其中download.py文件是主文件，运行它可以启动下载，目前仅提供activitynet和kinetics数据集的下载（持续更新），其实操作方式大同小异，具体操作方式是如下：

### 准备包含视频ID和URL的文件

最终视频的存放方式是：以视频ID为视频名，拓展名为.mp4，所有视频都存放在同一个文件夹下，不区分类别。比如activitynet和kinetics数据集是以.json文件方式提供ID和URL。

### 运行download.py文件
```shell
cd download
python download.py --dataset DATASET_NAME JSON_PATH FAILED_PATH --num_thread NUM_THREAD 
```
视频就保存在download.py所在文件夹。其中，DATASET_NAME, JSON_PATH，FAILED_PATH和NUM_THREAD分别表示所下载的数据集名称(在activity_net kinetics ava中选择)，json文件的存放位置，下载失败信息的保存位置，线程数(根据电脑配置和网络情况酌情选择，我设置在100左右)。

比如
```shell
python download.py --dataset kinetics ../kinetics_url/kinetics_400/kinetics_train/kinetics_train.json kinetics_train_failed.txt --num_thread 100
# 或者
python download.py --dataset activity_net ../activitynet_url/activity_net.v1-3.min.json activity_test_failed.txt --num_thread 10
```

