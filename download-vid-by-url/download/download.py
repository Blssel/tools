#coding:utf-8

uthor__='zhiyu yin'

import sys
import argparse
import youtube_dl
import threadpool
sys.path.append('..')
from parse_dataset import parse_json_file

def download(id_url):
    vid_id =id_url.split()[0]
    vid_url=id_url.split()[1]
      
    # 依据URL，下载数据（自动跳过并记录失败的数据）    
    # 选项解释https://github.com/rg3/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
    ydl_opts={
        'outtmpl':vid_id+'.mp4',
        #'format': 'bestvideo+bestaudio/best',
        # 'verbose': True,  # Print additional info to stdout.
        #'proxy': '127.0.0.1:8123',
        #'preferredquality': '480',
    }
  
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.extract_info(vid_url,download=True)
        except:
            print("!!!!!!------Download failed. Automatically ignoring and recoding its info------!!!!!!!")
            with open(args.failed_file,'a') as err:
                err.write(vid_id+ '  '+ vid_url+ '\n')



# 解析参数
def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('--dataset',dest='dataset',choices=['activity_net','kinetics','ava'],help='dataset name',default='activity_net')
    parser.add_argument('json_file',help='json file saving video ids and urls')
    parser.add_argument('failed_file',help='saving ulr whose video is unavailable')
    parser.add_argument('--num_thread',dest='num_thread',help='threads to work',default=1,type=int)
    args=parser.parse_args()
    
    return args


def main():
    # 解析参数
    global args
    args=parse_args()
    
    # 读取json或其他格式文件中的数据至一个video_list，video_list中的每一项都是一个ID和URL组合成的数组(id+'  '+url)
    # 解析依据数据集的不同而不同，但都统一使用parse_dataset()函数接口
    video_list=parse_json_file(args.dataset,args.json_file)

    # 多线程下载
    pool=threadpool.ThreadPool(args.num_thread)
    requests=threadpool.makeRequests(download,video_list)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    
    # 下载完成
    print 'download completed'

if __name__=='__main__':
    main()
