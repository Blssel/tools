#coding:utf-8

import os
import numpy as np
import cv2

VID_PATH='/share/dataset/20bn-something-something-v1'
SAVE_PATH='/home/yzy/dataset/ss'
for cur_path,dir_names,file_names in os.walk(VID_PATH):
	if len(file_names)==0:
		continue
		print 'hhh'
	else:
		vid_name=cur_path.split('/')[-1]+'.avi'
		#print vid_name
		fps=30.0
		framesize=cv2.imread(cur_path+os.sep+file_names[0]).shape
		#vid_writer=cv2.VideoWriter(SAVE_PATH+os.sep+vid_name,-1,fps,(framesize[0],framesize[1]),True)
		vid_writer=cv2.VideoWriter(SAVE_PATH+os.sep+vid_name,cv2.VideoWriter_fourcc(*'XVID'),fps,(framesize[0],framesize[1]),True)
		file_names.sort() #需要先排个序
		for img_name in file_names:
			print img_name
			img=cv2.imread(cur_path+os.sep+img_name)
			vid_writer.write(img)
		vid_writer.release()
